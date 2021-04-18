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
    correctness_threshold = 0.4
    def __init__(self):
        self.clothingRecModel = cr.ClothingRecognitionModel()
        self.webScraper = ws.WebScraper()
        if os.path.exists(os.path.join(os.path.dirname(__file__),storagefilename)):
            with open(storagefilename, 'rb') as handle:
                self.imageStorage = pickle.load(handle)

    @staticmethod
    def roundColor(color, base=50):
        r = int(base * round(color[0] / base))
        g = int(base * round(color[1] / base))
        b = int(base * round(color[2] / base))
        return r,g,b
    @staticmethod
    def getStorageKey(labels):
        if len(labels) == 2:
            key = ( (labels[0][0], VisualizerAPI.roundColor(labels[0][5])), 
                    (labels[1][0], VisualizerAPI.roundColor(labels[1][5])) )
        else:
            key = ( (labels[0][0], VisualizerAPI.roundColor(labels[0][5])) )
        print("storage key:", key)
        return key
    @staticmethod
    def colorError(c1, c2):
        error = 0
        for i in range(3):
            error += ((c1[i] - c2[i]) / 255) ** 2 
        # normalization (0 - 1)
        error /= 3
        if error < 0 or error > 1:
            print(1/0)
        return error

    @staticmethod
    def calculateCorrectness(label1, color1, label2, color2):
        correctness = 0
        for i, category in enumerate(label1):
            if category in label2:
                correctness += 0.5 ** (i + 1)
        correctness -= VisualizerAPI.colorError(color1, color2) / 10
        return correctness

    def getOutfitImgs(self, labels, num):
        outfits = []
        offset = 0
        if self.imageStorage.get(VisualizerAPI.getStorageKey(labels)) != None:
            outfits, offset = self.imageStorage[labels]
            if len(outfits) > num:
                outfits = outfits[:num]
        
        while len(outfits) < num:
            potential_outfits = self.webScraper.scrapeOutfits(labels, 2 * (num - len(outfits)) , offset) 
            for outfit in potential_outfits:
                offset += 1
                modelLabels, modelColors = self.clothingRecModel.getLabels(outfit)
                # make sure model agrees
                flat_labels = [item for sublist in modelLabels for item in sublist]

                total_correctness = 0
                # each article we are trying to match
                for article in labels:
                    # each proposed match 
                    article_correctness = 0
                    for j in range(len(modelLabels)):
                        #see how well it matches given article
                        correctness = VisualizerAPI.calculateCorrectness(article[:5], article[5], modelLabels[j], modelColors[j])
                        print("correctness:", correctness)
                        article_correctness = max(correctness, article_correctness)
                    total_correctness += article_correctness
                # normalize for number of articles
                total_correctness /= len(labels)

                if total_correctness >= self.correctness_threshold:
                    outfits.append(outfit)
                    if len(outfits) >= num:
                        break

        self.imageStorage[VisualizerAPI.getStorageKey(labels)] = (outfits, offset)

        return outfits
    
    def saveToDisk(self):
        with open(storagefilename, 'wb') as handle:
            pickle.dump(self.imageStorage, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    vapi = VisualizerAPI()
    outfitImages = vapi.getOutfitImgs((("Tee", "Flannel", "a", "b", "c", (255,255,255)), ("Jeans", "Leggings", "a", "b", "c", (0,0,254))), 5)
    outfitImages[0].save("test0.jpeg", format='jpeg')
    outfitImages[1].save("test1.jpeg", format='jpeg')
    vapi.saveToDisk()
    print("test completed.")