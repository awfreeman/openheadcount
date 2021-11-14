import cv2 as cv
import argparse
import imutils
import time
import numpy as np

confidence=0.1
frameskip=10
#load in network
model='mobnet/MobileNetSSD_deploy.caffemodel'
prototxt='mobnet/MobileNetSSD_deploy.prototxt'
net=cv.dnn.readNetFromCaffe(prototxt, model)

#list of classes that can be detected by model
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
#start video capture
vc = cv.VideoCapture("rtsp://admin:@192.168.1.224:554/h264Preview_01_main")
while vc.isOpened()==False:
    continue
skip=0
while True:
    rval, frame = vc.read()
    frame = imutils.resize(frame, width=1024, height=768)
    cv.imshow("preview", frame)
    key = cv.waitKey(20)
    if key == 27: # exit on ESC
        break
    if skip == frameskip:
        skip = 0
        presence = 0
        blob = cv.dnn.blobFromImage(image=frame, scalefactor=0.5, size=(1024,768))
        net.setInput(blob)
        outputs = net.forward()
        for i in np.arange(0, outputs.shape[2]):
            idx = int(outputs[0, 0, i, 1])
            if CLASSES[idx] == "person" and float(outputs[0, 0 , i , 2])>confidence:
                print(float(outputs[0, 0 , i , 2]))
                presence=presence+1
            
        print(presence)
    skip=skip+1
        
		

cv.destroyWindow("preview")
vc.release()
