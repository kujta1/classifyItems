from classifier import Classifier
from evaluate import Evaluation


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

        return None, None

    def generate_structure(self, item):
        # TODO
        # Vashiot KOD TUKA

        pass


evaluator = Evaluation(ClassifierOShporeti())
evaluator.evaluate_All_products()
