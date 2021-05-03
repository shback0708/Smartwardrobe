import sys
import os
from diskcache import Cache
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition/detector'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../clothing_recognition/classifier'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))

from clothing_recognition import clothing_recognizer as cr
import visualizer.webscraper as ws
# storagefilename = 'imagestorage.pickle'
tops = ['Anorak', 'Blouse', 'Blazer', 'Bomber', 'Button-Down', 'Cardigan', 'Coat', 'Flannel', 'Halter', 'Henley', 'Hoodie', 'Jacket', 'Jersey', 'Parka', 'Peacoat', 'Poncho', 'Sweater',  'Tank', 'Tee', 'Top', 'Turtleneck']
bottoms = ['Capris', 'Chinos', 'Culottes', 'Cutoffs', 'Gauchos', 'Jeans', 'Jeggings', 'Jodhpurs', 'Joggers', 'Leggings', 'Sarong', 'Shorts', 'Skirt', 'Sweatpants', 'Sweatshorts', 'Trunks']
onepieces = ['Caftan', 'Coverup', 'Dress', 'Jumpsuit', 'Kaftan', 'Kimono', 'Onesie', 'Robe', 'Romper']
class VisualizerAPI:
    imageStorage = None
    clothingRecModel = None
    webScraper = None
    correctness_threshold = 0.4
    def __init__(self):
        t0 = time.time()
        self.clothingRecModel = cr.ClothingRecognitionModel()
        t1 = time.time()
        self.webScraper = ws.WebScraper()
        t2 = time.time()
        # if os.path.exists(os.path.join(os.path.dirname(__file__),storagefilename)):
        #     with open(storagefilename, 'rb') as handle:
        #         self.imageStorage = pickle.load(handle)
        self.imageStorage = Cache("imagestorage")
        t3 = time.time()
        print("========setup benchmark========")
        print("clothing recognition model setup time: ", t1 - t0)
        print("webscraper setup time: ", t2 - t1)
        print("clothing image storage setup time: ", t3 - t2)
        print("total time: ", t3 - t0)
        time.sleep(3)
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
            print(labels)
            key = ( (labels[0][0], VisualizerAPI.roundColor(labels[0][5])) )
        print("storage key:", key)
        return key
    @staticmethod
    def colorError(c1, c2):
        print(c1,c2)
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

    # returns 0 if its a top, 1 if its a bottom, or 2 if its a one-piece
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

    def getOutfitImgs(self, labels, num):
        outfits = []
        offset = 0
        if self.imageStorage.get(VisualizerAPI.getStorageKey(labels)) != None:
            outfits, offset = self.imageStorage.get(VisualizerAPI.getStorageKey(labels))
            if len(outfits) > num:
                outfits = outfits[:num]
        
        while len(outfits) < num:
            print(num - len(outfits), "outfits left")
            potential_outfits = self.webScraper.scrapeOutfits(labels, int(1.5 * (num - len(outfits))) , offset)
            
            for index, result in enumerate(self.clothingRecModel.batchGetLabels(potential_outfits)):
                offset += 1

                total_correctness = 0
                # each article we are trying to match
                for article in labels:
                    # each proposed match 
                    article_correctness = 0
                    print("predictions: ")
                    for j in range(len(result)):
                        modelLabels = result[j][0]
                        modelProb   = result[j][1]
                        modelColors = result[j][2]
                        print("    ", modelLabels, modelProb, modelColors)
                        #see how well it matches given article
                        correctness = VisualizerAPI.calculateCorrectness(article[:5], article[5], modelLabels, modelColors)
                        print("correctness:", correctness)
                        article_correctness = max(correctness, article_correctness)
                    total_correctness += article_correctness
                # normalize for number of articles
                total_correctness /= len(labels)

                if total_correctness >= self.correctness_threshold:
                    outfits.append(potential_outfits[index])
                    if len(outfits) >= num:
                        break

        self.imageStorage[VisualizerAPI.getStorageKey(labels)] = (outfits, offset)

        return outfits
    
    def saveToDisk(self):
        # should be free
        self.imageStorage.close()
        return

if __name__ == '__main__':
    vapi = VisualizerAPI()
    time.sleep(3)
    amnt = 100
    outfitImages = vapi.getOutfitImgs((("Tee", "Flannel", "a", "b", "c", (255,255,255)), ("Jeans", "Leggings", "a", "b", "c", (0,0,254))), amnt)
    for i in range(3):
        for j in range(3):
            outfitImages = vapi.getOutfitImgs((("Dress", "Flannel", "a", "b", "c", (i*50,j*50,0)),), amnt)
            outfitImages[-1].save("dress" + str(i*10 + j) + ".jpeg", format='jpeg')
    assert(len(outfitImages) == amnt)
    vapi.saveToDisk()
    print("test completed.")