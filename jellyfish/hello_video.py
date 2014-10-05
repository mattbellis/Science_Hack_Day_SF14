import numpy as np
import cv2
import time
from collections import deque

#cap = cv2.VideoCapture('jellyfish_video.mp4')
cap = cv2.VideoCapture('jellyfish_video_longer.mp4')
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
print w,h

#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#fgbg = cv2.createBackgroundSubtractorMOG2()

fourcc = cv2.cv.CV_FOURCC(*'XVID')
#fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
fourcc = cv2.cv.CV_FOURCC(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 20, (w,h),True)
#out = cv2.VideoWriter('output.avi',-1, 24, (w,h),True)



ret, prev = cap.read()
icount = 0
#image_buffer = []
image_buffer = deque([])
while(cap.isOpened()):
    ret, frame = cap.read()

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if icount==0:
        image_buffer.append(frame)

    dst = frame
    if icount>100:
        dst = frame
        #print len(image_buffer)
        for i,img in enumerate(image_buffer):
            offset = (i/100.)*0.5
            #print offset
            if i<80:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                1
            dst = cv2.addWeighted(img,0.5-offset,dst,0.5+offset,0)
        dst = cv2.addWeighted(dst,0.70,frame,0.30,0)
        out.write(dst)
        image_buffer.popleft()

    #new_image = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    #new_image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    #new_image = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV)
    new_image = frame
    image_buffer.append(new_image)
    #image_buffer.append(frame)

    '''
    if icount>20:
        prev = image_buffer.popleft()
        dst = cv2.addWeighted(prev,0.5,frame,0.5,0)
        #prev = frame
    else:
        dst = frame
    '''

    cv2.imshow('frame',dst)

    #diff = frame - prev
    ##cv2.imshow('frame',gray)
    #cv2.imshow('frame',frame)
    #if icount>10:
        #cv2.imshow('frame',diff)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #time.sleep(0.01)
    #prev = frame

    icount += 1

cap.release()
out.release()
cv2.destroyAllWindows()
