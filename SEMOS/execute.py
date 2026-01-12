from ProductClassifier import ProductClassifier
from conf_file import openAi_key, groq_api
import json
from JsonProcessor import JsonPreprocessor

with open("categories.json", "r", encoding="utf-8") as f:
    categories = json.load(f)
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

class Execute:
    def __init__(self, products: list, category: dict, api_key: str):
        self.products = products
        self.category = category
        self.api_key = api_key
        self.preprocessor = JsonPreprocessor()
        self.num = 0

    @staticmethod
    def keyword_prefilter(category: dict, product: dict) -> bool:
        text = (
            product.get("description", "") +
            product.get("formatted_description", "") +
            product.get("breadcrumbs", "")
        ).lower()

        category_name = category.get("name", "").lower()
        return category_name in text

    def run(self) -> dict:
        positive = 0
        negative = 0
        skipped = 0

        for product in self.products:
            print(self.num)
            self.num += 1

            clean_product = self.preprocessor.normalize_product(product)

            # SKIP LLM CALL IF KEYWORDS DON'T MATCH
            if not self.keyword_prefilter(self.category, clean_product):
                skipped += 1
                continue

            matcher = ProductClassifier(
                self.category,
                clean_product,
                self.api_key,
            )

            if matcher.is_match():
                positive += 1
            else:
                negative += 1

        return {
            "positive_matches": positive,
            "negative_matches": negative,
            "skipped_no_llm": skipped
        }

if __name__ == "__main__":
    executor = Execute(
        products=products,
        category=categories[8],
        api_key = groq_api
    )

    result = executor.run()

    print(result)
