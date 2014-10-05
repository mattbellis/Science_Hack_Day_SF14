import numpy as np
import cv2


# Use 0 for the onboard webcam.
# Use 1 for an external webcam.
cap = cv2.VideoCapture(0)
print cap
if not cap:
    print "Error loading camera"
    exit(-1)

cap.open(0)
print cap
cv2.namedWindow("mywindow",)
print cap

while (cap.isOpened()):

    print cap

    ret,frame = cap.read()

    print ret
    print frame

    if ret==True:

        cv2.imshow('mywindow',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
#cv2.destroyAllWindows()
