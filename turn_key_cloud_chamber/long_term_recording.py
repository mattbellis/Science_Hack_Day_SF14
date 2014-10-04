import numpy as np
import cv2
import time
from subprocess import call

################################################################################
# Function to record data. Continue recording until we break it manually.
################################################################################
def record_data(camera_number=0,fps=24,seconds_before_trigger=3,seconds_after_trigger=3,fps_in_loop=20,threshold=1.8):

    mybuffer_len = fps_in_loop*(seconds_before_trigger+seconds_after_trigger)

    # List to store the images.
    images = []
    count = 0
    img = None
    start_of_images = 0

    cap = cv2.VideoCapture(0)

    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    #out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))

    ret,prev = cap.read()

    time_start=time.time()
    # while the user does not press 'esc'
    no_motion = True
    recording_after_trigger = False
    #while time.time()-time_start<SECONDS_TO_RECORD:
    recorded_time_after_trigger = False
    icount = 0
    trigger_event = False
    trigger_time = -999


    while (cap.isOpened()):
        ret,img = cap.read()

        if ret==True:

            if icount<mybuffer_len:
                #print "less than",icount,len(images)
                images.append(img.copy())
            else:
                #print "more than",icount,len(images)
                start_of_images = icount%mybuffer_len
                images[start_of_images] = img.copy()
             
            diff = cv2.absdiff(img,prev)
            mean = diff.mean()
            #print mean,threshold

            #cv2.imshow('img',img)
            cv2.imshow('diff',diff)

            #print icount,mean
            if mean>threshold and icount>20 and not trigger_event:
                no_motion = False
                trigger_event = True
                trigger_time = time.time()
                print "TRIGGER!"

            if trigger_event and time.time()-trigger_time>seconds_after_trigger:
                #write_out_event(images)
                trigger_event = False
                print "WRITING EVENT"
                buffer_name = "temp_output.avi"
                outname = 'output_{0}.mp4'.format(time.ctime().replace(" ", "_"))
                out = cv2.VideoWriter(buffer_name,fourcc,20.0,(640,480))
                '''
                for image in images:
                    #print type(image)
                    #cv2.imshow('image',image)
                    out.write(image)
                '''

                print "Processing the images."
                nimages = len(images)
                print "Images in this event %d" % (nimages)
                for i in range(start_of_images,start_of_images+nimages):
                    #i.save(disp)
                    myindex = i
                    #print myindex
                    if i>=nimages:
                        myindex = i-nimages
                    out.write(images[myindex])
                    #vs.writeFrame(images[myindex])


                params = " -i {0} -c:v mpeg4 -b:v 700k -r 24 {1}".format(buffer_name, outname)
                # run avconv to compress the video since ffmpeg is deprecated (going to be).
                call('avconv'+params, shell=True)
                out.release()

                icount = -1 # Because this will quickly get incremented
                del images
                images = []
                start_of_images = 0

                #exit()

            #out.write(img)

            prev = img
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            icount += 1

        else:
            break

    cap.release()
    #out.release()
    cv2.destroyAllWindows()


################################################################################
################################################################################
def main():

    camera_number =2
    record_data(camera_number=camera_number)

################################################################################
################################################################################
if __name__ == "__main__":
    main()


