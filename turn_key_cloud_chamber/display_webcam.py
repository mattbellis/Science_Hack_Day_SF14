# Import the parts we need from SimpleCV
from SimpleCV import Camera,VideoStream,Display,Color

# Imports to treat command line arguments 
import sys
from sys import argv
import getopt

FRAMES_PER_SECOND = 24

def main(cameraNumber, camWidth, camHeight):
    
    img = None

    # create a display with size (width, height)
    disp = Display((camWidth, camHeight))


    # Initialize Camera
    cam = Camera(cameraNumber, prop_set={"width": camWidth, "height": camHeight})

    while 1:
        # Finally let's started
        # KISS: just get the image... don't get fancy
    
        img = cam.getImage()

        img.show()


################################################################################
if __name__ == '__main__':
    HELP_MSG = '''record.py [options]

        -c &lt;cam NR&gt;   If you know which cam you want to use: set it here, else the first camera available is selected 

        -x &lt;cam Width&gt;    The width of camera capture. Default is 640 pixels
        --width

        -y &lt;cam Height&gt;   The height of camera capture. Default is 480 pixels
        --height

        -h &lt;help&gt;     Show this message
        '''


    # 0 for onboard webcam
    # 1 for external webcam
    camNR = 1
    width = 640
    height = 480

    try:
        opts, args = getopt.getopt(argv,"hx:y:c:",["width=","height="])
    except getopt.GetoptError:
        print HELP_MSG
        sys.exit(2)

    # Get the specified command line arguments  
    for opt, arg in opts:
        if opt == '-h':
            print HELP_MSG
            sys.exit()
        elif opt in ("-x", "--width"):
            width = arg
        elif opt in ("-y", "--height"):
            height = arg
        elif opt in ("-c"):
            camNR = arg
    
    main(camNR, width, height)
