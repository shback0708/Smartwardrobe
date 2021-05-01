from PIL import Image
class Classifier:
    def __init__(self):
        print("")

    def getAttributes(self,image):
        return (("Tee", "Tee", "Tee", "Tee", "Tee"), 1, (0,0,0))

class ClothingRecModel:
    classifier = Classifier()
    def __init__(self):
        classifier = Classifier()
    
class VisualizerAPI:

    clothingRecModel = ClothingRecModel()

    def __init__(self):
        clothingRecModel = ClothingRecModel()

    @staticmethod
    def getClothingType(category):
        if category in tops:
            return 0
        elif category in bottoms:
            return 1
        elif category in onepieces:
            return 2
        else:
            raise Exception("unknown clothing type: " + category)

    def getOutfitImgs(self, label, num):
        image = Image.open("00171615.jpg")
        return [image for i in range(num)]