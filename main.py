"""
    # main.py 
    main file of the project
"""
import cv2
#from app import run_gui
import motion_detect

def startMessage():
    print("\n+========================================+")
    print("| 2A2S: AI Augmented Surveillance System |")
    print("+========================================+\n")
    print("Loading, please wait...")

def main():
    #run_gui()

    cap = cv2.VideoCapture(0)

    motion_sensor = motion_detect.Motion_Detector(cap)
    motion_sensor.scanning_for_motion()



if (__name__ == "__main__"):
    startMessage()
    main()