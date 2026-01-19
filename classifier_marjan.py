import json
import re
from classifier_new import Classifier
from evaluate_new import Evaluation


class ClassifierFrizideri(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4d7",
                                     "67f71a03523d00258894a4d8"
        ],
                 classes_map={
                     "67f71a03523d00258894a4d7": "Фрижидери",
                     "67f71a03523d00258894a4d8": "Замрзнувачи"
                 }):
        super().__init__(
            classes_list=classes_list, classes_map=classes_map)

    def classify(self, item):
        breadcrumbs = item.get("Breadcrumbs", "")
        product_name = item.get("ProductName", "").lower()

        # Classifying as 'Фрижидери'
        if (re.search("фрижидер", breadcrumbs, re.IGNORECASE) or
            re.search("фрижидер", product_name, re.IGNORECASE) or
            re.search("ладилници", breadcrumbs, re.IGNORECASE) or
            re.search("ладилник", product_name, re.IGNORECASE)) and \
                not re.search("дополнителна опрема", breadcrumbs, re.IGNORECASE) and \
                not re.search("магнети", breadcrumbs, re.IGNORECASE) and \
                not re.search("Преносни фрижидери", breadcrumbs, re.IGNORECASE) and \
                not re.search("Акумулаторски фрижидер", product_name, re.IGNORECASE) and \
                not re.search("шпорет", product_name, re.IGNORECASE):
            return self.classes_list[0], self.classes_map[self.classes_list[0]]

        # Classifying as 'Замрзнувачи'
        elif re.search("замрзнувач", breadcrumbs, re.IGNORECASE) or re.search("замрзнувач", product_name,
                                                                              re.IGNORECASE):
            return self.classes_list[1], self.classes_map[self.classes_list[1]]

        else:
            return None, None


# Load the products data
with open('products.json', 'r', encoding='utf-8') as file:
    products_data = json.load(file)  # Assuming the products data is in JSON format

# Count the total number of products
total_products = len(products_data)
print("Total number of products:", total_products)

evaluator = Evaluation(ClassifierFrizideri())
evaluator.evaluate_All_products()
