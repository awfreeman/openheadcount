import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture("rtsp://admin:@192.168.1.186:554/h264Preview_01_main")

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()