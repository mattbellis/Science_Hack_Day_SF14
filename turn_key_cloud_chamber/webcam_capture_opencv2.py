import numpy as np
import cv2


# Use 0 for the onboard webcam.
# Use 1 for an external webcam.
cap = cv2.VideoCapture(1)
if not cap:
    print "Error loading camera"
    exit(-1)

cap.open(0)
cv2.namedWindow("mywindow",1)

while (cap.isOpened()):

    ret,frame = cap.read()

    if ret==True:

        cv2.imshow('mywindow',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()


