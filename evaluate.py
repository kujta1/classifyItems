import json
import re
from classifier import Classifier





class Evaluation():
    def __init__(self, classifier: Classifier, path_to_categories_file: str = './categories.json'):
        self.classifier = classifier
        json_file = open(path_to_categories_file, 'r', encoding='utf-8')
        categories_data = json.load(json_file)
        self.all_classes = {cat["_id"]: cat["name"] for cat in categories_data}

    def evaluate_item(self, item):
        predicted_class, _ = self.classifier.classify(item)
        labeled_category = item["Category"]
        if predicted_class is None and labeled_category is self.classifier.classes_list:
            return False, "other", labeled_category, item
        if predicted_class in self.classifier.classes_list and labeled_category not in self.classifier.classes_list:
            return False, predicted_class, labeled_category, item
        if predicted_class == labeled_category:
            return True, predicted_class, labeled_category, item
        else:
            return True, "other", "other", item

    def evaluate_All_products(self, path_to_items_file: str = './products.json'):
        results = []
        ista_klasa = 0
        razlichni_klasi = 0
        out_of_scope = 0
        ista_klasa_items = []
        razlichni_klasi_items = []

        with open(path_to_items_file, 'r', encoding='utf-8') as file:
            items_list = json.load(file)
        for item in items_list:
            prediction, predicted_class, labeled_class, item = self.evaluate_item(
                item)
            if prediction == True and predicted_class != "other":
                ista_klasa += 1
                ista_klasa_items.append(item)
            if prediction == False:
                razlichni_klasi += 1
                item["Category_predicted"] = predicted_class
                item["category_previously_human_readable"] = self.all_classes.get(
                    labeled_class, "other")
                item["category_predicted_human_readable"] = self.all_classes.get(
                    predicted_class, "other")
                if item.get("result") is None:
                    item["result"] = ""

                razlichni_klasi_items.append(item)

        with open('razlichni_klasi_items.json', 'w', encoding="utf-8") as f:
            json.dump(razlichni_klasi_items, f, indent=4, ensure_ascii=False)
        print("Ista klasa:", ista_klasa)
        print("Razlichni klasi:", razlichni_klasi)
        return results


