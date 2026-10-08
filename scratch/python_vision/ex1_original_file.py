# -- coding: utf-8 --
# src: https://github.com/ZhuWuyin/my-program/blob/master/ImageCompression/ImageCompression.py


from typing import Counter
import numpy as np
#import cv2

def avg(list1):
    return sum(list1)/len(list1)

def approximate(tolerance, list1):
    maxCounter=0
    maxList=[]

    counteri=0
    for i in list1:
        avgList=[]

        counteri+=1
        counterj=counteri
        counter=1
        for j in list1[counteri:]:

            interim=[]
            for k in range(len(i)):
                if i[k]-tolerance<j[k] and i[k]+tolerance>j[k]:
                    interim.append(j[k])

            if len(interim)==len(i):
                avgList.append(list1.pop(counterj))
                counter+=1
            else :
                counterj+=1

        if avgList:
            avgList.append(i)
            pixel=[]
            for num in range(len(i)):
                pixel.append(int(avg([val[num] for val in avgList])))
            if maxCounter<counter:
                maxCounter=counter
                maxList=pixel

    return maxList

def normalModel(list1, tolerance):
    pixelContainer=approximate(tolerance, list1)
    if pixelContainer:
        return pixelContainer
    else :
        return [int(avg([j[i] for j in list1])) for i in range(len(list1[0]))]

def compressPixel(pixel, tolerance, model):
    list1=[k for i in pixel for k in i]

    if model=="sharp":
        if len(list1)==len(set([str(i) for i in list1])):
            return normalModel(list1, tolerance)
        else :
            return eval(Counter([str(i) for i in list1]).most_common()[0][0])
    elif model=="normal" :
        return normalModel(list1, tolerance)
    else :
        return [int(avg([j[i] for j in list1])) for i in range(len(list1[0]))]

def getPixel(xShift, yShift, pixelWidth, pixelHeight, img):
    pixel=[]

    height=yShift+pixelHeight
    imgHeight=len(img)

    width=xShift+pixelWidth
    imgWidth=len(img[0])

    if height>imgHeight:
        pixelHeight-=height-imgHeight
    if width>imgWidth:
        pixelWidth-=width-imgWidth

    for i in range(yShift, yShift+pixelHeight):
        line=[]
        for j in range(xShift, xShift+pixelWidth):
            line.append(img[i][j])
        pixel.append(line)

    return pixel

if __name__ == "__main__":

    while True:

        imgPath=input("Image path (Drag the image here or type the path): ").replace("\\", "/")
        if imgPath[0]=='"':
            imgPath=imgPath[1:-1]

        outputName=input("Output image's name: ")+imgPath[imgPath.index("."):]

        outputPath=input("Target output path (Drag the document here or type the path): ").replace("\\", "/")
        if outputPath[0]=='"':
            outputPath=outputPath[1:-1]
        if outputPath[-1]!="/":
            outputPath+="/"

        im1=cv2.imdecode(np.fromfile(imgPath, dtype=np.uint8), -1).tolist()

        indexWidth=int(input("Width index: "))
        indexHeight=int(input("Height index: "))
        tolerance=int(input("Tolerance: "))

        while True:
            model=input("Process model(normal/sharp/quick): ").lower()
            if model=="normal" or model=="sharp" or model=="quick":
                break
            print("No such model")

        image=[]
        for i in range(0, len(im1), indexHeight):
            line=[]
            for j in range(0, len(im1[0]), indexWidth):
                line.append(compressPixel(getPixel(j, i, indexWidth, indexHeight, im1), tolerance, model))

            image.append(line)

        cv2.imencode(outputName, np.array(image, dtype=np.uint8))[1].tofile(outputPath+outputName)
        
        deterim=input("Image compressed successfully, do you want to continue? (Y/N)\n").lower()
        if deterim=='n':
            break