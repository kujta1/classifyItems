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
        pass
        #self.groq_client = GroqClient()