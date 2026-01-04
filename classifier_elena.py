from classifier import Classifier
from evaluate import Evaluation

class ClassifierOstanato(Classifier):
    def __init__(self, classes_list=None, classes_map=None):
        if classes_list is None:
            classes_list = ["67f71a03523d00258894a4e4", "67f71a03523d00258894a4e5"]
        if classes_map is None:
            classes_map = {
                "67f71a03523d00258894a4e4": "Аспиратори",
                "67f71a03523d00258894a4e5": "Бојлери"
            }
        super().__init__(classes_list, classes_map)

    def contains_keywords(self, text, keywords):
        return any(re.search(keyword, text, re.IGNORECASE) for keyword in keywords)

    def classify(self, item):
        breadcrumbs = item.get("Breadcrumbs", "")
        product_name = item.get("ProductName", "")
        formatted = item.get("FormattedDescription", "")

        aspirator_keywords = ["Аспиратори", "аспира"]
        boiler_keywords = [
            "Бојлери", "бојлер", "проточен бојлер",
            "Електрична чешма", "Електрична батерија",
            "Батерија високомонтажна", "Батерија нискомонтажна",
            "проточна", "елек.батерија"
        ]
        exclusion_keywords = ["Додатен прибор за аспиратори", "Филтер", "Дополнителна опрема"]

        if (self.contains_keywords(breadcrumbs, aspirator_keywords) or
                self.contains_keywords(product_name, aspirator_keywords)) and \
                not self.contains_keywords(breadcrumbs, exclusion_keywords) and \
                not self.contains_keywords(product_name, exclusion_keywords):
            return self.classes_list[0], self.classes_map[self.classes_list[0]]  # Аспиратори

        elif (self.contains_keywords(breadcrumbs, boiler_keywords) or
              self.contains_keywords(product_name, boiler_keywords) or 
              self.contains_keywords(formatted, boiler_keywords)):
            return self.classes_list[1], self.classes_map[self.classes_list[1]]  # Бојлери

        else:
            return None, None



    def generate_structure(self, item):
        # TODO
        # Vashiot KOD TUKA

        pass
evaluator = Evaluation(ClassifierOstanato())
evaluator.evaluate_All_products()
