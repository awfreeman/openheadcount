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
vc = cv.VideoCapture("yt1s.com - HD CCTV Camera video 3MP 4MP iProx CCTV HDCCTVCamerasnet retail store.mp4")
while vc.isOpened()==False:
    continue

objects = list()
skip=0
while True:
    rval, frame = vc.read()
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]
    key = cv.waitKey(20)
    if key == 27: # exit on ESC
        break
    if skip == frameskip:
        skip = 0
        #0.007843:normalizes values to between 0 and 2, 127.5: sets mean value to half brightness
        blob = cv.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
        net.setInput(blob)
        outputs = net.forward()

        newobjects = list()
        for i in np.arange(0, outputs.shape[2]):
            idx = int(outputs[0, 0, i, 1])
            if CLASSES[idx] == "person" and float(outputs[0, 0 , i , 2])>confidence:
                box = outputs[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                detections.append(box)
                frame = cv.rectangle(frame, pt1=(startX, startY), pt2=(endX,endY), color=(0,0,255), thickness=3)
        
        cv.imshow("funny", frame)
            
    skip=skip+1
        
		

cv.destroyWindow("preview")
vc.release()
