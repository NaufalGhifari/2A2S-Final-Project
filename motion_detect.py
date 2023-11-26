"""
    # motion_detect.py
    Temporary file to develop motion detection feature
"""

import threading
import cv2 as cv
import imutils

class Motion_Detector():
    """
        Configurable motion detector, linked to object detection model.
        Adapted from: https://www.youtube.com/watch?v=QPjPyUJeYYE&t=909s
    """
    def __init__(self, cap):
        self.cap = cap
        self.scanningIsON = False       # whether or not it is currently scanning for OBJECT
        self.scanning_mode = False      # whether or not it is currently scanning for MOTION
        self.scanning_counter = 0       # measures the amount of motion
        self.scanning_threshold = 20    # the amount of motion required to trigger scanningIsON
        
    def scanning_for_motion(self):
        # get the a first frame to compare later
        _, start_frame = self.cap.read()
        start_frame = imutils.resize(start_frame, width=500)
        start_frame = cv.cvtColor(start_frame, cv.COLOR_BGR2GRAY)
        start_frame = cv.GaussianBlur(start_frame, (21, 21), 0)

        while True:
            # get another frame to compare
            _, frame = self.cap.read()
            frame = imutils.resize(frame, width=500)

            # only run when motion scanning is on
            if self.scanning_mode: 
                frame_bw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                frame_bw = cv.GaussianBlur(frame_bw, (5, 5), 0)

                difference = cv.absdiff(frame_bw, start_frame)
                threshold = cv.threshold(difference, 25, 255, cv.THRESH_BINARY)[1] # below 25 -> 0, above 25 -> 255
                start_frame = frame_bw

                # if theres movement above a certain value, increase scanning_counter
                if threshold.sum() > 300:
                    self.scanning_counter += 1
                else:
                    # reduce back to 0 if we dont see enough movement
                    if self.scanning_counter > 0:
                        self.scanning_counter -= 1

                cv.imshow("Cam", threshold) # show black and white vision
            
            else:
                cv.imshow("Cam", frame) # show normal vision
            
            # trigger object detection if motion is beyond threshold 
            if self.scanning_counter > self.scanning_threshold:
                self.scanningIsON = True
                threading.Thread(target=self.trigger_object_scanning).start()
            
        # =================================================
        # TODO: REMOVE
            key_pressed = cv.waitKey(30)
            if key_pressed == ord("t"):
                self.scanning_mode = not self.scanning_mode
                self.scanning_counter = 0
            if key_pressed == ord("q"):
                self.scanning_mode = False
                break

        self.cap.release()
        cv.destroyAllWindows()
        # ==================================================

    def trigger_object_scanning(self):
        for i in range(5):
            if not self.scanning_mode:
                break
            else:
                # DO SCANNING STUFF HERE
                print("### ! SCANNING TRIGGERED ", i,  " ! ###")
        
        # switch back to off
        self.scanningIsON = False

"""==================================================================================================================="""

"""
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv.cvtColor(start_frame, cv.COLOR_BGR2GRAY)
start_frame = cv.GaussianBlur(start_frame, (21, 21), 0)

scanningIsON = False
scanning_mode = False
scanning_counter = 0

def trigger_scanning():
    global scanning

    for i in range(5):
        if not scanning_mode:
            break
        else:
            print("### ! SCANNING TRIGGERED ", i,  " ! ###")
    
    scanningIsON = False

while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if scanning_mode:
        frame_bw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_bw = cv.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv.absdiff(frame_bw, start_frame)
        threshold = cv.threshold(difference, 25, 255, cv.THRESH_BINARY)[1]
        start_frame = frame_bw

        # if theres movement above a certain value, increase scanning_counter
        if threshold.sum() > 300:
            scanning_counter += 1
        else:
            # reduce back to 0 if we dont see enough movement
            if scanning_counter > 0:
                scanning_counter -= 1

        cv.imshow("Cam", threshold)
    else:
        cv.imshow("Cam", frame)
    
    if scanning_counter > 20:
        scanningIsON = True
        threading.Thread(target=trigger_scanning).start()

    key_pressed = cv.waitKey(30)
    if key_pressed == ord("t"):
        scanning_mode = not scanning_mode
        scanning_counter = 0
    if key_pressed == ord("q"):
        scanning_mode = False
        break

cap.release()
cv.destroyAllWindows()
"""

        