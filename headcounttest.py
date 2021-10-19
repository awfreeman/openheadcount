import cv2 as cv
import argparse
import imutils

model='mobnet/MobileNetSSD_deploy.caffemodel'
prototxt='mobnet/MobileNetSSD_deploy.prototxt'
net=cv.dnn.readNetFromCaffe(prototxt, model)