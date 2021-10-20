import cv2 as cv
import argparse
import imutils

model='mobnet/MobileNetSSD_deploy.caffemodel'
prototxt='mobnet/MobileNetSSD_deploy.prototxt'
#load in network
net=cv.dnn.readNetFromCaffe(prototxt, model)
#start video capture
vc = cv.VideoCapture("rtsp://admin:@192.168.1.186:554/h264Preview_01_main")
while vc.isOpened()==False:
    continue
while True:
    rval, frame = vc.read()
    frame = imutils.resize(frame, width=640, height=480)
    rgb=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    blob=cv.dnn.blobFromImage(frame)
cv2.destroyWindow("preview")
vc.release()
