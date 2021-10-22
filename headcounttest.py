import cv2 as cv
import argparse
import imutils
import time
import numpy as np

model='mobnet/MobileNetSSD_deploy.caffemodel'
prototxt='mobnet/MobileNetSSD_deploy.prototxt'
#load in network
net=cv.dnn.readNetFromCaffe(prototxt, model)
#start video capture
#list of classes that can be detected by model
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
vc = cv.VideoCapture("rtsp://admin:@192.168.1.186:554/h264Preview_01_main")
while vc.isOpened()==False:
    continue
while True:
    rval, frame = vc.read()
    frame = imutils.resize(frame, width=320, height=240)
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    blob = cv.dnn.blobFromImage(image=frame, scalefactor=0.5, size=(320,240))
    net.setInput(blob)
    outputs = net.forward()
    cv.imshow("preview", frame)
    key = cv.waitKey(20)
    if key == 27: # exit on ESC
        break
    presence=False
    for i in np.arange(0, outputs.shape[2]):
        idx = int(outputs[0, 0, i, 1])
        if CLASSES[idx] == "person":
            presence = True
    if presence:
        print("there a dude in der")
    else:
        print("nobody here")
        
		

cv.destroyWindow("preview")
vc.release()
