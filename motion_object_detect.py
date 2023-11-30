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
from datetime import date

class Motion_Object_Detector():
    """
        Motion and Object detector class.
        1. Constantly scanning for movement 
        2. If movement is detcted, run object detection for 5 seconds

        Input argument: cap -> a cv2.VideoCapture() object as input.
    """
    def __init__(self, cap):
        self.cap = cap
        self.frame = None

        self.is_scanning_objects = False    # whether or not it is currently scanning for OBJECT
        self.is_scanning_motion = False     # whether or not it is currently scanning for MOTION
        self.scanning_counter = 0           # measures the amount of motion
        self.scanning_threshold = 20        # the amount of motion required to trigger self.is_scanning_objects
        self.scan_duration = 5              # how long obj det model runs

        self.motion_logs_path = 'motion_log.txt'
        self.object_logs_path = 'object_log.txt'
        self.motion_log = None
        self.object_logs = None

        self.initialise_object_detector('yolov8n.pt')
        self.initialise_log_file()
    
    ### MOTION DETECTION ### ===================================================================================================== #
    ### Adapted with modifications from: https://www.youtube.com/watch?v=QPjPyUJeYYE&t=909s

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
            if self.is_scanning_motion: 
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
            
            ####################### OBJECT DETECION STARTS HERE ###################################
            if self.scanning_counter > self.scanning_threshold:
                self.is_scanning_objects = True
                self.write_motion_logs()
                self.start_object_detector()

                """ threading.Thread(target=self.start_object_detector).start() """ # does not work for now
                            
        # =================================================
        # TODO: 1. Link to GUI
        # TODO: 2. REMOVE
            key_pressed = cv2.waitKey(30)
            if key_pressed == ord("t"):
                print("T pressed")
                self.is_scanning_motion = not self.is_scanning_motion
                self.scanning_counter = 0
            if key_pressed == ord("q"):
                self.is_scanning_motion = False
                break

        self.cap.release()
        cv2.destroyAllWindows()
        # ==================================================

    ### LOG FILES ### =================================================================================================================== #
    def initialise_log_file(self):
        """Prepare log files for motion and object detection"""
        try:
            self.motion_log = open(self.motion_logs_path, 'a')
            self.object_log = open(self.object_logs_path, 'a')
        
        except Exception as err:
            print("Unexpected error occured during motion log writing: ", err)
        else:
            print("Log files initialised successfully.")

    # IMPROVE: Fine tune log writing, maybe only write every second or minute
    def write_motion_logs(self):
        """Handles log writing when MOTION is detected"""

        curr_date, curr_time = self.get_curr_date_time()
        motion_log_entry = f"Motion detected at {curr_time} on {curr_date}\n"
        self.motion_log.write(motion_log_entry)
    
    # TODO: Write a log for object detection
    def wrie_object_logs(self):
        """Handles log writing when OBJECT is detected"""
        pass

    def get_curr_date_time(self):
        """Returns the current date and current time"""
        t = time.localtime()
        curr_time = time.strftime("%H:%M:%S", t)
        curr_date = date.today()

        return curr_date, curr_time

    
    
    ### OBJECT DETECTION ### ============================================================================================================= #
    # Adapted with modifications from: https://www.youtube.com/watch?v=QV85eYOb7gk&t=726s

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
            self.is_scanning_objects = False

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