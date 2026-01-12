import json
from  Objekt import Product
import re

#("Шпорети",  "Вградливи фурни и плотни", "Вградливи рерни",           "Вградливи плотни",  "Вградливи сетови од рерна и плотна",           "Микробранови печки")
def classify(product):

    if re.search("Вградливи сетови од рерна и плотна",product.get("Breadcrumbs"),re.IGNORECASE):
        return ("Вградливи сетови од рерна и плотна")
    elif re.search("Вградливи фурни и плотни",product.get("Breadcrumbs"),re.IGNORECASE):
        return ("Вградливи фурни и плотни")
    elif re.search("Вградливи рерни",product.get("Breadcrumbs"),re.IGNORECASE):
        return ("Вградливи рерни")
    elif re.search("Вградливи плотни",product.get("Breadcrumbs"),re.IGNORECASE):
        return ("Вградливи плотни")
    elif re.search("Микробранови печки", product.get("Breadcrumbs"), re.IGNORECASE):
        return ("Микробранови печки")
    elif re.search("Шпорети", product.get("Breadcrumbs"), re.IGNORECASE):
        return ("Шпорети")
    else:
        return ("None")




def list_products():
    with open("products.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for item in data:
        category=classify(item)
        print(category)

list_products()



