import os
import shutil

import csv
from glob import glob
import os.path
import random

labelsfile = "data/train_labels.csv"
testlabelsfile = "data/test_labels.csv"
traindir = "data/train/"
valdir = "data/validate/"
testdir = "data/test/"
random.seed(18500)
# with open(labelsfile) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     #ignore column names
#     row_num = -1
#     for row in csv_reader:
#         row_num += 1
#         if row_num == 0:
#             continue
#         if row_num % 10000 == 0:
#             print("finished", row_num)

#         if random.random() > (20/90):
#             destdir = traindir
#         else:
#             destdir = valdir

#         label = row[1]
#         image_path = "data/" + row[0]
#         filename = str(row_num).zfill(8) + ".jpg"
#         try:
#             os.mkdir(destdir + label)
#         except:
#             pass

#         shutil.copy(image_path, destdir + label + "/" + filename)

with open(testlabelsfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #ignore column names
    row_num = -1
    for row in csv_reader:
        row_num += 1
        if row_num == 0:
            continue
        if row_num % 10000 == 0:
            print("finished", row_num)

        destdir = testdir
        
        label = row[1]
        image_path = "data/" + row[0]
        filename = str(row_num).zfill(8) + ".jpg"
        try:
            os.mkdir(destdir + label)
        except:
            pass

        shutil.copy(image_path, destdir + label + "/" + filename)


    