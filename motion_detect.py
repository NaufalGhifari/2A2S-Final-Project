"""
    # motion_detect.py
    Temporary file to develop motion detection feature
"""

import threading
import cv2
import imutils
from ultralytics import YOLO
import supervision as sv
import torch
import time

class Motion_Detector():
    """
        Configurable motion detector, linked to object detection model.
        Adapted from: https://www.youtube.com/watch?v=QPjPyUJeYYE&t=909s
    """
    def __init__(self, cap):
        self.cap = cap
        self.frame = None

        self.scanningIsON = False       # whether or not it is currently scanning for OBJECT
        self.scanning_mode = False      # whether or not it is currently scanning for MOTION
        self.scanning_counter = 0       # measures the amount of motion
        self.scanning_threshold = 20    # the amount of motion required to trigger scanningIsON
        self.scan_duration = 5

        self.initialise_object_detector('yolov8n.pt')
        
    def scanning_for_motion(self):
        # get the a first frame to compare later
        success, start_frame = self.cap.read()
        
        print("[DEBUG] Motion_Detector.motion_cap.type() = ", type(self.cap))
        print("[DEBUG] Motion_Detector.start_frame.type() = ", type(start_frame))
        print("[DEBUG] Motion_Detector.success.type() = ", type(success), success)
        
        if not self.cap.isOpened():
            print("Error opening video feed")

        if success:
            start_frame = imutils.resize(start_frame, width=500)
            start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
            start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
        else:
            print("Unable to capture first comparison frame")

        while True:
            # get another frame to compare
            success, self.frame = self.cap.read()
            if success:
                self.frame = imutils.resize(self.frame, width=500)
            else:
                print("Unable to capture second comparison frame")

            # only run when motion scanning is on
            if self.scanning_mode: 
                frame_bw = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

                difference = cv2.absdiff(frame_bw, start_frame)
                threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1] # below 25 -> 0, above 25 -> 255
                start_frame = frame_bw

                # if theres movement above a certain value, increase scanning_counter
                if threshold.sum() > 300:
                    self.scanning_counter += 1
                else:
                    # reduce back to 0 if we dont see enough movement
                    if self.scanning_counter > 0:
                        self.scanning_counter -= 1

                cv2.imshow("Cam", self.frame) # show black and white vision
            
            else:
                cv2.imshow("Cam", self.frame) # show normal vision
            
            # OBJECT DETECION STARTS HERE
            if self.scanning_counter > self.scanning_threshold:
                self.scanningIsON = True
                self.start_object_detector()

                """ threading.Thread(target=self.start_object_detector).start() """ # does not work for now
                            
        # =================================================
        # TODO: 1. Link to GUI
        # TODO: 2. REMOVE
            key_pressed = cv2.waitKey(30)
            if key_pressed == ord("t"):
                self.scanning_mode = not self.scanning_mode
                self.scanning_counter = 0
            if key_pressed == ord("q"):
                self.scanning_mode = False
                break

        self.cap.release()
        cv2.destroyAllWindows()
        # ==================================================

# ====================================================================================================================
    # Object detection part

    def gpu_check(self):
            """Checks if a GPU is available. Returns boolean."""
            if torch.cuda.is_available():
                print("CUDA (GPU) is available. Version: ", torch.version.cuda)
                return True
            else:
                print("CUDA (GPU) is not available. Using CPU.")
                return False

    def start_object_detector(self):
        results = self.model(self.frame)[0]
        detections = sv.Detections.from_ultralytics(results)

        scan_start_time = time.time() # get current time
        self.scan_for_objects(detections, scan_start_time)
    
    def scan_for_objects(self, detections, scan_start_time):

        if time.time() - scan_start_time < self.scan_duration:
            # annotate images
            self.frame = self.boxAnnotator.annotate(
                scene=self.frame,
                detections=detections
            )

            cv2.imshow("Cam", self.frame)
            print("Obj Det is running.")

        else:
            self.scanningIsON = False

    def initialise_object_detector(self, model):
        # load model
        try:
            model_path = model
            self.model = YOLO(model_path)
        except IOError as err:
            print("[!] Error occured while loading model: ", err)
            return
        
        # use GPU if available
        if(self.gpu_check() == True):
            print("Switching to GPU...")
            self.model.to('cuda')
        
        # setup supervision BoxAnnotator
        self.boxAnnotator = sv.BoxAnnotator(
            thickness = 2,
            text_thickness = 2,
            text_scale = 1
        )