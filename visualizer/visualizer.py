import sys
import os
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition/detector'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition/classifier'))

from clothing_recognition import clothing_recognizer as cr
import webscraper as ws
storagefilename = 'imagestorage.pickle'
class VisualizerAPI:
    imageStorage = {}
    clothingRecModel = None
    webScraper = None
    def __init__(self):
        self.clothingRecModel = cr.ClothingRecognitionModel()
        self.webScraper = ws.WebScraper()
        if os.path.exists(os.path.join(os.path.dirname(__file__),storagefilename)):
            with open(storagefilename, 'rb') as handle:
                self.imageStorage = pickle.load(handle)

    def getOutfitImgs(self, labels, num):
        if self.imageStorage.get(labels) == None:
            outfits = []
            potential_outfits = self.webScraper.scrapeOutfits(labels, num)
            for outfit in potential_outfits:
                modelLabels, modelColors = self.clothingRecModel.getLabels(outfit)
                # make sure model agrees
                correct = True
                for label in labels:
                    flat_labels = [item for sublist in modelLabels for item in sublist]
                    if label[0] not in flat_labels:
                        print("missing", label[0])
                        correct = False
                        break
                
                if correct:
                    outfits.append(outfit)

            self.imageStorage[labels] = outfits
        else:
            outfits = self.imageStorage[labels]
        return outfits
    
    def saveToDisk(self):
        with open(storagefilename, 'wb') as handle:
            pickle.dump(self.imageStorage, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    vapi = VisualizerAPI()
    outfitImages = vapi.getOutfitImgs((("Tee", "Flannel", "a", "b", "c", (255,255,255)), ("Jeans", "Leggings", "a", "b", "c", (0,0,255))), 5)
    outfitImages[0].save("test0.jpeg", format='jpeg')
    outfitImages[1].save("test1.jpeg", format='jpeg')
    vapi.saveToDisk()
    print("test completed.")