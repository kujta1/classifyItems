import json
import re

def classify(product):
    if re.search("Фрижидери",product.get("Breadcrumbs"),re.IGNORECASE):
        return ("Фрижидери")
    elif re.search("Замрзнувачи",product.get("Breadcrumbs"),re.IGNORECASE):
        return ("Замрзнувачи")
    else:
        return None

def list_products():
    with open("products.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for item in data:
        category=classify(item)
        print(category)

list_products()