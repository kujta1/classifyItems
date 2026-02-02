from classifier import Classifier
from evaluate import Evaluation
import re


class ClassifierOShporeti(Classifier):
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
        # TODO
        #finshed
        # Vashiot KOD TUKA
        if re.search("Вградливи сетови од рерна и плотна",item.get("Breadcrumbs"),re.IGNORECASE):
            return ("Вградливи сетови од рерна и плотна")
        elif re.search("Вградливи фурни и плотни",item.get("Breadcrumbs"),re.IGNORECASE):
            return ("Вградливи фурни и плотни")
        elif re.search("Вградливи рерни",item.get("Breadcrumbs"),re.IGNORECASE):
            return ("Вградливи рерни")
        elif re.search("Вградливи плотни",item.get("Breadcrumbs"),re.IGNORECASE):
            return ("Вградливи плотни")
        elif re.search("Микробранови печки", item.get("Breadcrumbs"), re.IGNORECASE):
            return ("Микробранови печки")
        elif re.search("Шпорети", item.get("Breadcrumbs"), re.IGNORECASE):
            return ("Шпорети")
        else:
            return ("None")
        

    def generate_structure(self, item):
        # TODO
        # Vashiot KOD TUKA

        pass


evaluator = Evaluation(ClassifierOShporeti())
evaluator.evaluate_All_products()
