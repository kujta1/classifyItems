from classifier import Classifier
from evaluate import Evaluation


class ClassifierMashini(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4db", "67f71a03523d00258894a4da", "67f71a03523d00258894a4dc"],
                 classes_map={"67f71a03523d00258894a4db": "mashini za perenje",
                              "67f71a03523d00258894a4da": "mashini za sushenje",
                              "67f71a03523d00258894a4dc": "mashini za perenje i sushenje"}
                 ):
        super().__init__(classes_list, classes_map)

    def classify(self, item):
        # TODO
        # Vashiot KOD TUKA

        return None, None

    def generate_structure(self, item):
        # TODO
        # Vashiot KOD TUKA

        pass


evaluator = Evaluation(ClassifierMashini())
evaluator.evaluate_All_products()
