from classifier import Classifier
from evaluate import Evaluation
import json
import re
from typing import Any, Dict, Optional


class Classifier:
    def __init__(
        self,
        classes_list: Optional[list] = None,
        classes_map: Optional[dict] = None,
        groq_client: Any = None,
    ):
        self.classes_list = classes_list or []
        self.classes_map = classes_map or {}
        # Optional Groq client. If None, generate_structure() will return None.
        self.groq_client = groq_client

    def classify(self, item: Dict[str, Any]) -> str:
        raise NotImplementedError

    def generate_structure(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Optional: call Groq to return structured JSON.

        Returns:
            Parsed JSON dict on success, None if groq_client is not available.
        """
        if not self.groq_client:
            return None

        product_name = str(item.get("ProductName", ""))
        breadcrumbs = str(item.get("Breadcrumbs", ""))
        desc = str(item.get("FormattedDescription", ""))

        prompt = f"""
Classify this product into exactly ONE of the following category IDs:

- 67f71a03523d00258894a4da = Машини за перење алишта (WASH_ONLY)
- 67f71a03523d00258894a4db = Машини за сушење алишта (DRY_ONLY)
- 67f71a03523d00258894a4dc = Перење & Сушење 2-in-1 (WASH_DRY_COMBO)
- 67f71a03523d00258894a4dd = Машини за миење садови (DISHWASHER)
- останати = OTHER

Rules:
1) Choose COMBO only if strong evidence of BOTH washing and drying (e.g., пере и суши, перење и сушење, 2 во 1, 2 in 1, washer dryer, WD model codes).
2) Choose DRY_ONLY only if it clearly refers to a dryer appliance (e.g., сушара, машина за сушење, dryer, heat pump dryer, кондензациона сушара).
   Do NOT choose DRY_ONLY just because the text mentions "сушење" as a feature.
3) Choose WASH_ONLY if it is a washing machine and not a combo.
4) Choose DISHWASHER if it is about dishes (садови, dishwasher).

Return JSON ONLY in this schema:
{{
  "category_id": "...",
  "confidence": 0.0,
  "reasons": ["...", "..."],
  "signals": {{
    "found_keywords": ["..."],
    "model_hint": "..."
  }}
}}

Product:
- ProductName: {product_name}
- Breadcrumbs: {breadcrumbs}
- FormattedDescription: {desc}
""".strip()

        response = self.groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON. No extra text."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # If the model returns extra text, keep raw for debugging.
            return {"raw": content}


class ClassifyMashini(Classifier):
    """Regex-based appliance classifier for washer/dryer/dishwasher categories."""

    # Category IDs (the project IDs)
    CAT_WASH_ONLY_ID = "67f71a03523d00258894a4da"
    CAT_DRY_ONLY_ID = "67f71a03523d00258894a4db"
    CAT_WASH_DRY_ID = "67f71a03523d00258894a4dc"
    CAT_DISHWASHER_ID = "67f71a03523d00258894a4dd"
    CAT_OTHER_ID = "останати"

    def __init__(self, classes_list=None, classes_map=None, groq_client: Any = None):
        super().__init__(classes_list=classes_list, classes_map=classes_map, groq_client=groq_client)

        # NOTE: DRY_ONLY intentionally does NOT match the bare word "сушење" to avoid false positives.
        self.patterns = {
            "DISHWASHER": re.compile(r"\b(dishwasher)\b|машина\s*за\s*садови|миење\s*садови|\bсадови\b", re.IGNORECASE),
            "WASH_DRY": re.compile(
                r"пере\s*и\s*суши|перење\s*и\s*сушење|2\s*во\s*1|2\s*in\s*1|2in1|washer\s*dryer|wash\s*\+\s*dry|комбинирана\s*машина|\bcombo\b",
                re.IGNORECASE,
            ),
            "DRY_ONLY": re.compile(
                r"сушара|машина\s*за\s*сушење|\b(dryer|tumble\s*dryer)\b|топлинска\s*пумпа|heat\s*pump|кондензац",
                re.IGNORECASE,
            ),
            "WASH_ONLY": re.compile(
                r"машина\s*за\s*перење|\b(washing\s*machine)\b|перална|\bперење\b",
                re.IGNORECASE,
            ),
        }

    def classify(self, item: Dict[str, Any]) -> str:
        text_to_scan = (
            f"{item.get('ProductName', '')} {item.get('Breadcrumbs', '')} {item.get('FormattedDescription', '')}"
        ).lower()

        # Priority order matters.
        if self.patterns["DISHWASHER"].search(text_to_scan):
            return self.CAT_DISHWASHER_ID

        if self.patterns["WASH_DRY"].search(text_to_scan):
            return self.CAT_WASH_DRY_ID

        if self.patterns["DRY_ONLY"].search(text_to_scan):
            return self.CAT_DRY_ONLY_ID

        if self.patterns["WASH_ONLY"].search(text_to_scan):
            return self.CAT_WASH_ONLY_ID

        return self.CAT_OTHER_ID

