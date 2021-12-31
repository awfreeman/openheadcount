import cv2 as cv
import argparse
import imutils
import time
import numpy as np
from centroidtracker import Tracker

CONFIDENCE=0
#load in network
MODEL='mobnet/MobileNetSSD_deploy.caffemodel'
PROTOTXT='mobnet/MobileNetSSD_deploy.prototxt'
#list of classes that can be detected by model
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
#start video capture
vc = cv.VideoCapture("vid.mp4")
while vc.isOpened()==False:
    continue
#initialize network
net=cv.dnn.readNetFromCaffe(PROTOTXT, MODEL)

track=Tracker(15, 3)
objects = list()
while True:
    rval, frame = vc.read()
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]
    key = cv.waitKey(20)
    if key == 27: # exit on ESC
        break
    #0.007843:normalizes values to between 0 and 2, 127.5: sets mean value to half brightness
    blob = cv.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
    net.setInput(blob)
    outputs = net.forward()
    
    newobjects = list()
    for i in np.arange(0, outputs.shape[2]):
        idx = int(outputs[0, 0, i, 1])
        if CLASSES[idx] == "person" and float(outputs[0, 0 , i , 2])>CONFIDENCE:
            #get new centroids
            box = outputs[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = box.astype("int")
            #add new centroids to list
            newobjects.append(((startX+endX)//2,(startY+endY)//2))
            
            #frame = cv.rectangle(frame, pt1=(startX, startY), pt2=(endX,endY), color=(0,0,255), thickness=3)
            #frame = cv.circle(frame, newobjects[-1], radius=3, color=(0,255,0), thickness=-1)
    track.update(newobjects)
    for x in track.objects:
        frame = cv.circle(frame, x[0], radius=3, color=(0,255,0), thickness=-1)
        frame = cv.putText(frame, str(x[2]), x[0], cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 6)
    
    cv.imshow("preview", frame)
		

cv.destroyWindow("preview")
vc.release()
