import urllib.request
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import numpy as np
import cv2 as cv
from os import listdir
import pickle
from sklearn.preprocessing import LabelBinarizer

def downloadData(txtFile, label):
    path = os.path.join("./dataset", label)
    os.mkdir(path)
    with open(txtFile) as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        url = line
        count+=1
        filePath = "./dataset/" + label + "/" + label + str(count) +".jpg"
        try:
            print("File: ",filePath)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with open(filePath, "wb") as f:
                with urllib.request.urlopen(req) as r:
                    f.write(r.read())
        except:
            continue
    f.close()

def createData():
    labels = ["banh_xeo", "banh_bot_loc", "banh_trung_thu", "banh_khot", "banh_cong", "banh_tai_heo", "banh_da_lon", "banh_tieu", "banh_bo", "banh_com"]
    for label in labels :
        txtFile = "./textFile/" + label +".txt"
        downloadData(txtFile, label)

def saveData(rawFolder):
    kichThuocAnh = (256, 256)
    print("Bắt đầu xử lí...")
    images = []
    labels = []

    for folder in listdir(rawFolder):
        print("Folder=",folder)
        for file in listdir(rawFolder  + folder):
            print("File=", file)
            img = cv.imread(rawFolder  + folder +"/" + file)
            images.append(cv.resize(cv.cvtColor(img, cv.COLOR_BGR2RGB),dsize=(256,256)))
            labels.append(folder)
    images = np.array(images)
    labels = np.array(labels) #.reshape(-1,1)
    encoder = LabelBinarizer()
    labels = encoder.fit_transform(labels)
    print(labels)

    file = open('./dataset/vietnamese_foods.data', 'wb')
    pickle.dump((images,labels), file)
    file.close()
    return 


def main():
    isCreateData = False
    if isCreateData:
        createData()
    else:
        saveData("./dataset/")


if __name__ == "__main__":
    main()