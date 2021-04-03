import sys
import os
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition/clothing_recognition'))

storagefilename = 'imagestorage.pickle'
class VisualizerAPI:
    imageStorage = {}
    clothingRecModel = None
    webScrapper = None
    def __init__(self):
        self.clothingRecModel = ClothingRecognitionModel()
        with open('filename.pickle', 'rb') as handle:
            self.imageStorage = pickle.load(storagefilename)

    def getOutfitImgs(self, labels, num):
        if self.imageStorage.get(labels) == None:
            outfits = self.webSrapper.scrapeOutfits(labels, num)
            self.imageStorage[labels] = outfits
        else:
            outfits = self.imageStorage[labels]
        return outfits
    
    def saveToDisk(self):
        with open(storagefilename, 'wb') as handle:
            pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    vapi = VisualizerAPI()
    print("test completed.")