import json

class JsonPreprocessor:
    def __init__(self, max_text_length: int = 2000):
        self.max_text_length = max_text_length

    def normalize_product(self, product: dict) -> dict:
        return {
            "name": product.get("ProductName", ""),
            "breadcrumbs": product.get("Breadcrumbs", ""),
            "description": self._truncate(product.get("Description", "")),
            "formatted_description": self._truncate(product.get("FormattedDescription", ""))
        }

    def normalize_category(self, category: dict) -> dict:
        return {
            "name": category.get("name", ""),
            "description": category.get("description", ""),
            "tags": category.get("tags", [])
        }

    def normalize_categories(self, categories: list) -> list:
        return [self.normalize_category(cat) for cat in categories]

    def _truncate(self, text: str) -> str:
        return text[:self.max_text_length]
