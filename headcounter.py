import cv2 as cv
import argparse
import imutils
import time
import numpy as np
import threading
from centroidtracker import Tracker

CONFIDENCE=.4
PATH = "vid.mp4"

#load in network
MODEL='mobnet/MobileNetSSD_deploy.caffemodel'
PROTOTXT='mobnet/MobileNetSSD_deploy.prototxt'

#list of classes that can be detected by model
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
class headcounter:
    def __init__(self):
        self.stop = False
        self.track = None
        self.outputframe = None
    def run(self, stoplock, getlock, imglock, path, vertexes, threshold, history):
        with imglock:
            vc = cv.VideoCapture(path)
            while vc.isOpened()==False:
                continue
        
        #initialize network and centroid tracker
        net=cv.dnn.readNetFromCaffe(PROTOTXT, MODEL)
        self.track = Tracker(threshold, history, vertexes)
        while True:
            with stoplock:
                if self.stop:
                    vc.release()
                    return None
            rval, frame = vc.read()
            if frame is None:
                vc = cv.VideoCapture(path)
                while vc.isOpened()==False:
                    continue
                rval, frame = vc.read()
            frame = imutils.resize(frame, width=500)
            (H, W) = frame.shape[:2]
            
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
                    
            
            #update tracker with new objects
            with getlock:
                self.track.update(newobjects)

            #draw centroids and ID's 
            for x in self.track.objects:
                frame = cv.circle(frame, x[0], radius=3, color=(0,255,0), thickness=-1)
                #frame = cv.putText(frame, str(x[2]), x[0], cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 6)
            
            #draw line
            for x in range(0, len(vertexes)):
                frame = cv.line(frame, vertexes[x], vertexes[x-1], (255,0,0), 4)
            

            for x in self.track.objects:
                if x[3]:
                    frame = cv.putText(frame, "In", x[0], cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 6)
                else:
                    frame = cv.putText(frame, "Out", x[0], cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 6)
            frame = cv.putText(frame, str(self.track.count), (0, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 6)
            with imglock:
                self.outputframe = frame.copy()
            cv.pollKey()
        vc.release()