from classifier import Classifier

from evaluate import Evaluation


class ClassifierFrizideri(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4d7",
                                     "67f71a03523d00258894a4d8",
                                     ], classes_map={
        "67f71a03523d00258894a4d7": "Фрижидери",
        "67f71a03523d00258894a4d8": "Замрзнувачи",
    }
    ):
        super().__init__(
            classes_list=classes_list, classes_map=classes_map)

    def classify(self, item):
        # TODO
        # Vashiot KOD TUKA

        return None, None

    def generate_structure(self, item):
        # TODO
        # Vashiot KOD TUKA

        pass


evaluator = Evaluation(ClassifierFrizideri())
evaluator.evaluate_All_products()
