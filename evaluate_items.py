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

    def classify(self, item):
        pass
    def generate_structure(self, item):
        self.groq_clien=GroqClient()


class ClassifyFridzandLadilinici(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4d8",
                                     "67f71a03523d00258894a4d7",
                                     ], classes_map={
        "67f71a03523d00258894a4d7": "Фрижидери",
        "67f71a03523d00258894a4d8": "замрзнувачи",
    }
    ):
        super().__init__(
            classes_list=classes_list, classes_map=classes_map)

    def classify(self, item):
        # if re.search("Фрижидери со замрзнувач на горна страна", item.get("Breadcrumbs"), re.IGNORECASE):
        #     return self.classes_list[0], self.classes_map[self.classes_list[0]]
        # elif re.search("Фрижидери со замрзнувач на долна страна", item.get("Breadcrumbs"), re.IGNORECASE):
        #     return self.classes_list[1], self.classes_map[self.classes_list[1]]
        # else:
        return None, None


class ClassifyShporeti(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4de",
                                     "67f71a03523d00258894a4e2",
                                     "67f71a03523d00258894a4df",
                                     "67f71a03523d00258894a4e3",
                                     "67f71a03523d00258894a4e1",
                                     "67f71a03523d00258894a4e0"
                                     ], classes_map={
        "67f71a03523d00258894a4de": "Шпорети",
        "67f71a03523d00258894a4e2": "Вградливи сетови од рерна и плотна",
        "67f71a03523d00258894a4df": "Вградливи фурни и плотни",
        "67f71a03523d00258894a4e3": "Микробранови печки",
        "67f71a03523d00258894a4e1": "Вградливи плотни",
        "67f71a03523d00258894a4e0": "Вградливи рерни"
    }
    ):
        super().__init__(
            classes_list=classes_list, classes_map=classes_map)

    def classify(self, item):
        if re.search("Шпорети", item.get("Breadcrumbs"), re.IGNORECASE):
            return self.classes_list[0], self.classes_map[self.classes_list[0]]
        elif re.search("Вградливи сетови од рерна и плотна", item.get("Breadcrumbs"), re.IGNORECASE):
            return self.classes_list[1], self.classes_map[self.classes_list[1]]
        elif re.search("Вградливи фурни и плотни", item.get("Breadcrumbs"), re.IGNORECASE):
            return self.classes_list[2], self.classes_map[self.classes_list[2]]
        elif re.search("Вградливи рерни", item.get("Breadcrumbs"), re.IGNORECASE):
            return self.classes_list[5], self.classes_map[self.classes_list[5]]
        elif re.search("Вградливи плотни", item.get("Breadcrumbs"), re.IGNORECASE):
            return self.classes_list[4], self.classes_map[self.classes_list[4]]
        elif re.search("Микробранови печки", item.get("Breadcrumbs"), re.IGNORECASE):
            return self.classes_list[3], self.classes_map[self.classes_list[3]]
        else:
            return None, None


class ClassifyMаshini(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4db", "67f71a03523d00258894a4da", "67f71a03523d00258894a4dc"],
                 classes_map={"67f71a03523d00258894a4db": "mashini za perenje",
                              "67f71a03523d00258894a4da": "mashini za sushenje",
                              "67f71a03523d00258894a4dc": "mashini za perenje i sushenje"}
                 ):
        super().__init__(classes_list, classes_map)

    def classify(self, item):
        ###
        ###
        # return None, None # ako ne e od ednata od classite, kako shto vikavme porano Others
        return "67f71a03523d00258894a4da", self.classes_map["67f71a03523d00258894a4da"]


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


evaluator = Evaluation(ClassifyFRidz())
evaluator.evaluate_All_products()
