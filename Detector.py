"""


SYNTAX NOTE: 
    - Snake case is preferred for general use due to its readability. 
    - Camelcase is reserved for Booleans to help with comprehension speed.
"""

import cv2
import supervision as sv
from ultralytics import YOLO
from datetime import datetime, date, timedelta, time
from PIL import Image, ImageTk
import Email_Alert
import torch

class Detector_2A2S:
    
    # INITIALISATION ======================================================================================================
    def __init__(self, cap):
        
        # define the VideoCapture object
        self.cap = cap

        # PARAMETERS: bg subtraction
        self.bg_sub_threshold = 30
        self.hist = 150
        self.bg_subtract = cv2.createBackgroundSubtractorMOG2(history=self.hist, varThreshold=self.bg_sub_threshold, detectShadows=False)

        # PARAMETERS: frame diff
        self.frame_diff_threshold = 100

        # PARAMETERS: contours
        self.min_contour_size = 500

        # PARAMETERS: log files
        self.motion_logs_path = "./logs/motion_log.txt"
        self.motion_frames_path = "./logs/motion_frames/"
        self.object_logs_path = "./logs/object_log.txt"
        self.object_frames_path = "./logs/object_frames/"
        self.last_log_time = datetime.now() - timedelta(minutes=2) # make sure it starts writing at minute 0

        # PARAMETERS: object detection
        self.objectDetectionIsON = False
        self.obj_scan_duration = 30
        self.obj_scan_time_start = datetime.now()
        self.model_path = "yolov8n.pt"

        # PARAMETERS: Alert system
        self.alert_time_start = "20:00"
        self.alert_time_end = "08:00"
        self.isSendingAlerts = False
        self.user_alerter = Email_Alert.email_alert_system()

        # PARAMETERS: export to GUI
        self.export_frame = None

        # init object detection attributes
        self.initialise_object_detector()

        # list of objects that can be detected by yolov8 (COCO dataset)
        self.object_classes_id = {
            0: 'person',
            1: 'bicycle',
            2: 'car',
            3: 'motorcycle',
            4: 'airplane',
            5: 'bus',
            6: 'train',
            7: 'truck',
            8: 'boat',
            9: 'traffic light',
            10: 'fire hydrant',
            11: 'stop sign',
            12: 'parking meter',
            13: 'bench',
            14: 'bird',
            15: 'cat',
            16: 'dog',
            17: 'horse',
            18: 'sheep',
            19: 'cow',
            20: 'elephant',
            21: 'bear',
            22: 'zebra',
            23: 'giraffe',
            24: 'backpack',
            25: 'umbrella',
            26: 'handbag',
            27: 'tie',
            28: 'suitcase',
            29: 'frisbee',
            30: 'skis',
            31: 'snowboard',
            32: 'sports ball',
            33: 'kite',
            34: 'baseball bat',
            35: 'baseball glove',
            36: 'skateboard',
            37: 'surfboard',
            38: 'tennis racket',
            39: 'bottle',
            40: 'wine glass',
            41: 'cup',
            42: 'fork',
            43: 'knife',
            44: 'spoon',
            45: 'bowl',
            46: 'banana',
            47: 'apple',
            48: 'sandwich',
            49: 'orange',
            50: 'broccoli',
            51: 'carrot',
            52: 'hot dog',
            53: 'pizza',
            54: 'donut',
            55: 'cake',
            56: 'chair',
            57: 'couch',
            58: 'potted plant',
            59: 'bed',
            60: 'dining table',
            61: 'toilet',
            62: 'tv',
            63: 'laptop',
            64: 'mouse',
            65: 'remote',
            66: 'keyboard',
            67: 'cell phone',
            68: 'microwave',
            69: 'oven',
            70: 'toaster',
            71: 'sink',
            72: 'refrigerator',
            73: 'book',
            74: 'clock',
            75: 'vase',
            76: 'scissors',
            77: 'teddy bear',
            78: 'hair drier',
            79: 'toothbrush'
        }
    
    def gpu_check(self):
            """
            Checks if a GPU is available. 
            
            Return: Boolean"""
            if torch.cuda.is_available():
                print("CUDA (GPU) is available. Version: ", torch.version.cuda)
                return True
            else:
                print("CUDA (GPU) is not available. Using CPU.")
                return False

    def initialise_object_detector(self):
        """
        1. Loads object detection model (.pt file)
        2. Employs GPU if available
        3. Setup box annotator for objec detections
        
        Return: Void
        """
        # load model
        try:
            self.model = YOLO(self.model_path)
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
    
    def reset_obj_detector_timer():
        pass

    def check_isSendingAlerts(self, now=datetime.now().time()):
        """
        Checks if self.isSendingAlerts should be True or False depending on the current time.
        Return: Boolean
        """
        # get the hour and minute in int
        # ERROR: FIX THIS by turning it into a str first (maybe)
        start_hour = int(str(self.alert_time_start).split(":")[0])
        start_min = int(str(self.alert_time_start).split(":")[1])
        end_hour = int(str(self.alert_time_end).split(":")[0])
        end_min = int(str(self.alert_time_end).split(":")[1])

        # process the times
        start = time(hour=start_hour, minute=start_min, second=00)
        end = time(hour=end_hour, minute=end_min, second=00)
        #now = datetime.now().time()

        if start < end:
            return start <= now <= end
        else:
            return now >= start or now <= end
    
    def get_export_frame(self):
        """
        Retrieves latest frame to use in GUI

        Return: image object
        """
        return self.export_frame

    # MOTION ============================================================================================================
    def motion_object_scanner(self):
        
        while True:
            # check current time to send alerts or not
            if self.check_isSendingAlerts() == True:
                self.isSendingAlerts = True
            else:
                self.isSendingAlerts = False

            # reset motion detection flag for each frame
            self.motionIsDetected = False

            try:
                _, frame = self.cap.read()
            except Exception as err:
                print(f"[!] Motion scanner error: {err}")

            # convert frame to grayscale
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # comparing current and previous frame
            if 'prev_frame' in locals():
                frame_diff = cv2.absdiff(prev_frame, frame_gray)
            else:
                frame_diff = cv2.absdiff(frame_gray, frame_gray)
            
            # define next iteration's 'prev_frame'
            prev_frame = frame_gray 

            # bg subtraction
            foreground = self.bg_subtract.apply(frame_gray)

            # combine bg subtraction with frame diff
            combined_frame = cv2.bitwise_and(frame_diff, foreground)
            _, combined_frame = cv2.threshold(combined_frame, self.frame_diff_threshold, 255, cv2.THRESH_BINARY)

            # contouring motion
            contours_array, _ = cv2.findContours(combined_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # OBJ DETECTION ====================================================================================================
            # if objectDetectionIsON, scan for objects. Otherwise, scan for motion 
            if self.objectDetectionIsON:
                
                # only run object detection model for 30 seconds
                scan_obj_elapsed_time = datetime.now() - self.obj_scan_time_start
                remaining_time = max(self.obj_scan_duration - scan_obj_elapsed_time.total_seconds(), 0)
                cv2.putText(frame, f"[Scanning for OBJECTS ({remaining_time:.0f}s)]", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
                
                if(scan_obj_elapsed_time > timedelta(seconds=self.obj_scan_duration)):
                    self.objectDetectionIsON = False
                    print(f"Switching to MOTION detection (self.objectDetectionIsON = False)")
                
                # TODO: do object detection here
                results = self.model.predict(frame, stream=True, verbose=False)[0]
                detections = sv.Detections.from_ultralytics(results)

                # debug
                print(detections)
                print(f"detections:\n {detections.class_id}")
                if len(detections.class_id) > 0:
                    print("Detection array is NOT empty")

                    named_objects= [self.object_classes_id[i] for i in detections.class_id]
                    print(f"named detections:\n {named_objects}")
                else:
                    print("Detection array is empty")

                frame = self.boxAnnotator.annotate(
                    scene = frame,
                    detections = results
                )  
                
            # MOTION DETECTION =================================================================================================
            else:
                cv2.putText(frame, "[Scanning for MOTION]", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                for c in contours_array:
                    size = cv2.contourArea(c)
                    if (size >= self.min_contour_size):
                        # draw motion boxes
                        (x, y, w, h) = cv2.boundingRect(c)                    
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # add text top right corner
                        cv2.putText(frame, "[!] Motion Detected.", (5, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                        
                        # write log
                        self.write_motion_logs(frame)

                        # switch to OBJ DETECTION
                        self.objectDetectionIsON = True    
                
                if self.objectDetectionIsON:
                    self.obj_scan_time_start = datetime.now()
                    print(f"Switching to OBJ detection (self.objectDetectionIsON = True)")

                    # send email alert
                    if self.isSendingAlerts:
                        self.user_alerter.send_alert_cli("motion", datetime.now())

            # export to GUI
            self.export_frame = frame

            # display feed
            """ cv2.imshow("2A2S", frame) """

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
    # LOGS ====================================================================================================================================
    def get_curr_date_time(self):
        """Returns the current date and current time"""
        curr_time = datetime.now().strftime("%H:%M:%S")
        curr_date = date.today()
        return curr_date, curr_time

    def write_motion_logs(self, frame):
        """
        - Handles log writing when MOTION is detected
        - Saves current frame to "/logs/motion_frames/"

        Return: Void
        """
        
        # only write once every minute
        current_time = datetime.now()
        if(current_time - self.last_log_time >= timedelta(minutes=1)):
            
            with open(self.motion_logs_path, "a") as motion_log:
                # set new last_log_time
                self.last_log_time = current_time 

                # write log
                curr_date, curr_time = self.get_curr_date_time()
                motion_log_entry = f"Motion detected at {curr_time} on {curr_date}\n"
                motion_log.write(motion_log_entry)
            
            # saving frame as png
            timestamp = str(datetime.now())[:19].replace(":",";").replace(" ", "_") # replace chars to make sure filename is valid
            filename = self.motion_frames_path + timestamp + ".png"
            saved = cv2.imwrite(filename, frame)
            if saved:
                print(f"\nMotion frame saved successfully to {filename}")
            else:
                print(f"\nError occured when saving motion frame to: {filename}\n")
            

    def write_object_logs(self):
        # TODO: write function
        pass

    # USER ALERT SYSTEM ======================================================================================================================

def main():
    cap = cv2.VideoCapture(0)
    app = Detector_2A2S(cap)
    app.motion_object_scanner()

    cap.release()
    cv2.destroyAllWindows() 

if __name__ == '__main__':
    main()
