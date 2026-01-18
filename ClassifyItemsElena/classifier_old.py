import json
import re


class Classifier():
    def __init__(self, classes_list=None, classes_map=None):
        """
        Za koi classsi napravivme classifier
        primer za classfier_mashini
        classes_list=["67f71a03523d00258894a4db",
            "67f71a03523d00258894a4da", "67f71a03523d00258894a4dc"]
        classes_map={"67f71a03523d00258894a4db":"mashini za perenje",
                     "67f71a03523d00258894a4da":"mashini za sushenje",
                     "67f71a03523d00258894a4dc":"mashini za perenje i sushenje"}

        Args:
            classes_list (_type_, optional): _description_. Defaults to None.
            classes_map (_type_, optional): _description_. Defaults to None.
        """
        self.classes_list = classes_list
        self.classes_map = classes_map

class ClassifierOstanato(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4e4",
                                     "67f71a03523d00258894a4e5",
                                     ], classes_map={
        "67f71a03523d00258894a4e4": "Аспиратори",
        "67f71a03523d00258894a4e5": "Бојлери",
    }
    ):
        super().__init__(
            classes_list=classes_list, classes_map=classes_map)
    
    def classify(self, item):
        breadcrumbs = item.get("Breadcrumbs", "")
        # product_name = item.get("ProductName", "")

        if re.search("Аспиратори", breadcrumbs, re.IGNORECASE):
            return self.classes_list[0], self.classes_map[self.classes_list[0]]
        
        elif re.search("Бојлери", breadcrumbs, re.IGNORECASE):
            return self.classes_list[1], self.classes_map[self.classes_list[1]]
        
        else:
            return None, None
        


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
        filtered_products = []

        with open(path_to_items_file, 'r', encoding='utf-8') as file:
            items_list = json.load(file)
        for item in items_list:
            prediction, predicted_class, labeled_class, item = self.evaluate_item(item)
            if prediction == True and predicted_class != "other":
                ista_klasa += 1
                item["Category_predicted"] = predicted_class
                item["category_previously_human_readable"] = self.all_classes.get(labeled_class, "other")
                item["category_predicted_human_readable"] = self.all_classes.get(predicted_class, "other")
                if item.get("result") is None:
                    item["result"] = ""
                ista_klasa_items.append(item)
                
                # Store filtered products
                filtered_products.append(item)

            if prediction == False:
                razlichni_klasi += 1
                item["Category_predicted"] = predicted_class
                item["category_previously_human_readable"] = self.all_classes.get(labeled_class, "other")
                item["category_predicted_human_readable"] = self.all_classes.get(predicted_class, "other")
                if item.get("result") is None:
                    item["result"] = ""
                razlichni_klasi_items.append(item)


        with open('razlichni_klasi_items_old.json', 'w', encoding="utf-8") as f:
            json.dump(razlichni_klasi_items, f, indent=4, ensure_ascii=False)
        print("Ista klasa:", ista_klasa)
        print("Razlichni klasi:", razlichni_klasi)

        with open('ista_klasa_items_old.json', 'w', encoding="utf-8") as f:
            json.dump(ista_klasa_items, f, indent=4, ensure_ascii=False)    
        
        return results
    

evaluator = Evaluation(ClassifierOstanato())
evaluator.evaluate_All_products()
