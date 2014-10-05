import numpy as np
import cv2
import cv2.cv as cv
import time



# Use 0 for the onboard webcam.
# Use 1 for an external webcam.
#cap = cv2.VideoCapture("jellyfish_video.mp4")
cap = cv2.cv.CaptureFromFile("jellyfish_video.mp4")
#print cap.grab()

nframes=int(cv2.cv.GetCaptureProperty(cap,cv2.cv.CV_CAP_PROP_FRAME_COUNT))

print nframes

prev = cv.QueryFrame(cap)
for f in xrange(nframes):
    frameimg=cv.QueryFrame(cap)
    print " currpos of videofile",cv.GetCaptureProperty(cap,cv.CV_CAP_PROP_POS_MSEC)
    print " index of frame",cv.GetCaptureProperty(cap,cv.CV_CAP_PROP_POS_FRAMES)
    print type(frameimg)
    diff = frameimg - prev
    cv.ShowImage("hcq",diff)
    #cv.ShowImage("hcq",frameimg)
    time.sleep(0.5)
    cv.WaitKey(1)

