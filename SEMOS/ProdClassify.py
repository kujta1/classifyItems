"""
GroqCategoryMatcher

A Python class that uses a Groq LLM to decide whether each product JSON object
matches a category name. The class is written to handle 2k-3k objects by batching
and concurrency, with retries and exponential backoff.

Notes:
- You must set the GROQ_API_KEY environment variable or pass api_key explicitly.
- The default GROQ API endpoint is set to the common /v1/outputs pattern; adjust
  GROQ_API_URL if your account uses a different endpoint.
- The LLM is asked to return a small JSON blob per product so results are easy to parse.

Example:
    matcher = GroqCategoryMatcher(api_key="sk-...")
    result = matcher.count_matches(category_json, products_list)
    print(result["count"], result["matches"][:5])
"""
from __future__ import annotations
import os
import asyncio
import aiohttp
import json
import time
from conf_file import groq_api
from typing import List, Dict, Any, Optional, Tuple

class GroqCategoryMatcher:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "groq-1",
        concurrency: int = 6,
        batch_size: int = 1,
        remove_description: bool = True,
        groq_api_url: str = "https://api.groq.ai/v1/outputs",
        request_timeout: int = 30,
        max_retries: int = 3,
        backoff_base: float = 1.0,
    ):
        """
        api_key: Groq API key (or set GROQ_API_KEY env var)
        model: model name to use (e.g. "groq-1")
        concurrency: number of parallel requests (keep reasonable for rate limits)
        batch_size: number of products to send per LLM call (1 recommended for highest fidelity)
        remove_description: if True, remove the `Description` field from the payload sent to the LLM
        groq_api_url: endpoint to call (adjust if Groq endpoint differs)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key not provided; set api_key or GROQ_API_KEY env var.")
        self.model = model
        self.concurrency = concurrency
        self.batch_size = max(1, batch_size)
        self.remove_description = remove_description
        self.groq_api_url = groq_api_url
        self.request_timeout = request_timeout
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        # semaphore to limit concurrency
        self._sem = asyncio.Semaphore(self.concurrency)

    async def _call_groq_once(self, session: aiohttp.ClientSession, prompt: str) -> str:
        """
        Make a single HTTP call to Groq LLM. Adjust payload structure if your Groq API differs.
        This function returns a plain text response (attempts to extract text from common fields).
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            # Many Groq examples accept `input` or `prompt`. We include `input` as a single-string payload.
            "input": prompt,
            # Some deployments can accept additional options; add here if needed.
        }

        async with session.post(self.groq_api_url, json=payload, headers=headers, timeout=self.request_timeout) as resp:
            text = await resp.text()
            # try to parse JSON and extract common fields
            try:
                j = json.loads(text)
                # Common patterns: "output", "outputs", "choices", "results"
                if isinstance(j, dict):
                    if "output" in j:
                        # Could be string or list
                        out = j["output"]
                        if isinstance(out, list):
                            return " ".join([str(x) for x in out])
                        return str(out)
                    if "outputs" in j:
                        # Newer APIs return list of outputs
                        outs = j["outputs"]
                        if isinstance(outs, list) and len(outs) > 0:
                            # try text / content
                            first = outs[0]
                            # try a few common keys
                            for key in ("content", "text", "output", "message"):
                                if isinstance(first, dict) and key in first:
                                    v = first[key]
                                    if isinstance(v, list):
                                        return " ".join([str(x) for x in v])
                                    return str(v)
                            return json.dumps(first)
                    if "choices" in j:
                        choices = j["choices"]
                        if isinstance(choices, list) and len(choices) > 0:
                            c0 = choices[0]
                            for key in ("text", "message", "output"):
                                if key in c0:
                                    return str(c0[key])
                            return json.dumps(c0)
                # fallback to raw text if JSON doesn't contain expected fields
                return text
            except Exception:
                # not JSON or parse failed; return raw text
                return text

    async def _call_groq_with_retries(self, session: aiohttp.ClientSession, prompt: str) -> str:
        """
        Retry logic with exponential backoff.
        """
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                async with self._sem:
                    return await self._call_groq_once(session, prompt)
            except Exception as e:
                last_exc = e
                wait = self.backoff_base * (2 ** (attempt - 1))
                await asyncio.sleep(wait)
        # If we exhausted retries, raise the last exception
        raise last_exc

    def _build_prompt(self, category_name: str, product: Dict[str, Any]) -> str:
        """
        Build a concise prompt that asks the model to answer with a small JSON object.
        The LLM will be asked to return exactly:
        {"match": true/false, "reason": "<short explanation>"}

        We include only a few fields to reduce token usage.
        """
        p = product.copy()
        if self.remove_description:
            # drop long free-form Description to save tokens
            if "Description" in p:
                p.pop("Description", None)
            if "description" in p:
                p.pop("description", None)

        # Include only most relevant keys (safe defaults)
        fields_to_include = ["ProductName", "ProductUrl", "StoreName", "Breadcrumbs", "FormattedDescription", "Category", "_id"]
        included = {k: p.get(k, "") for k in fields_to_include if k in p or k in p.keys()}

        # Prepare prompt
        prompt = (
            f"You are a strict classifier. Decide whether the product below belongs to the category "
            f"named: \"{category_name}\".\n\nProduct (JSON):\n{json.dumps(included, ensure_ascii=False)}\n\n"
            "Answer with a single JSON object only, with these exact keys:\n"
            '{"match": true|false, "reason": "<one-sentence justification (<= 30 words)>"}\n\n'
            "Do NOT output any other text. Be conservative: if uncertain, return match: false."
        )
        return prompt

    async def _classify_product(self, session: aiohttp.ClientSession, category_name: str, product: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Use LLM to classify a single product. Returns (match_boolean, reason).
        """
        prompt = self._build_prompt(category_name, product)
        raw = await self._call_groq_with_retries(session, prompt)
        # Try to extract JSON from the model response
        # The model is asked to return only JSON, but guard against extra text.
        try:
            # find first '{' and last '}' to extract JSON
            first = raw.find("{")
            last = raw.rfind("}")
            if first != -1 and last != -1 and last > first:
                candidate = raw[first:last+1]
                j = json.loads(candidate)
            else:
                # fallback: try to parse the whole response
                j = json.loads(raw)
            match = bool(j.get("match", False))
            reason = str(j.get("reason", "") or "")
            return match, reason
        except Exception:
            # If parsing fails, conservatively treat as not matched and return raw text as reason
            return False, f"LLM response parse failed: {raw[:200].replace(chr(10), ' ')}"

    async def _process_batch(self, session: aiohttp.ClientSession, category_name: str, batch: List[Dict[str, Any]]) -> List[Tuple[str, bool, str]]:
        """
        Process a batch (list) of product dicts. Returns list of tuples (product_id, match, reason).
        By default we classify one-by-one inside the batch; this is easiest for deterministic parsing.
        You can modify to send multiple products in one prompt to save calls (but parsing becomes more complex).
        """
        results = []
        for prod in batch:
            prod_id = prod.get("_id", prod.get("ProductUrl", "<no-id>"))
            try:
                match, reason = await self._classify_product(session, category_name, prod)
            except Exception as e:
                match = False
                reason = f"error: {e}"
            results.append((prod_id, match, reason))
        return results

    async def count_matches_async(self, category_json: Dict[str, Any], products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Asynchronous implementation that iterates over all products and returns a report:
        {
            "category_name": "...",
            "total_products": N,
            "count": M,
            "matches": [ { "id": "...", "reason": "..." }, ... ],
            "non_matches": [ ... ]
        }
        """
        num = 0
        category_name = category_json.get("name") or category_json.get("Name") or ""
        if not category_name:
            raise ValueError("category_json must include a 'name' field with the category name.")

        timeout = aiohttp.ClientTimeout(total=self.request_timeout + 10)
        connector = aiohttp.TCPConnector(limit=self.concurrency * 2)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            tasks = []
            # Create batches
            batches = [products[i:i + self.batch_size] for i in range(0, len(products), self.batch_size)]
            results = []
            # Process batches sequentially or concurrently based on concurrency setting
            # We'll schedule all batches but the semaphore in _call_groq_with_retries will throttle to concurrency.
            for batch in batches:
                tasks.append(self._process_batch(session, category_name, batch))

            # gather with concurrency control via semaphore inside calls
            for fut in asyncio.as_completed(tasks):
                print(num)
                num += 1
                batch_res = await fut
                results.extend(batch_res)

        matches = [{"id": pid, "reason": reason} for (pid, match, reason) in results if match]
        non_matches = [{"id": pid, "reason": reason} for (pid, match, reason) in results if not match]

        return {
            "category_name": category_name,
            "total_products": len(products),
            "count": len(matches),
            "matches": matches,
            "non_matches": non_matches,
        }

    def count_matches(self, category_json: Dict[str, Any], products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronous wrapper over count_matches_async.
        """
        return asyncio.run(self.count_matches_async(category_json, products))


# Example usage:
if __name__ == "__main__":
    with open("categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    # Simple local test (replace with real API key or set Groq env var)
    sample_category = {
        "_id": "67f71a03523d00258894a4dc",
        "name": "Машини за перење и сушење алишта",
        "description": "Combined washer-dryer machines ...",
        "parent_id": "67f71a03523d00258894a4d9",
    }

    sample_products = [
        {
            "_id": "p1",
            "ProductName": "Bosch WNG254A0BY",
            "FormattedDescription": "Bosch washer dryer combo, 10kg wash / 6kg dry, VarioPerfect, AutoDry.",
            "Breadcrumbs": "Vudelgo-Bosch-Пере и Суши 2 in 1-Перење и сушење на алишта-",
        },
        {
            "_id": "p2",
            "ProductName": "Some other product",
            "FormattedDescription": "A small toaster oven.",
            "Breadcrumbs": "Vudelgo-Kitchen-Останато-",
        },
    ]

    # Provide API key via env var or pass to constructor
    api_key = os.getenv("GROQ_API_KEY", None)
    matcher = GroqCategoryMatcher(api_key=groq_api, concurrency=4, batch_size=1, remove_description=True)

    # Run (this will call the Groq LLM; ensure credentials and endpoint are correct)
    try:
        report = matcher.count_matches(categories[8], products)
        print("Report:", json.dumps(report, ensure_ascii=False, indent=2))
    except Exception as exc:
        print("Error running GroqCategoryMatcher:", exc)