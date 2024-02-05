import cv2
from ultralytics import YOLO
from datetime import datetime, date, timedelta
import emailAlert

class mySurveillanceClass:
    
    # INITIALISATION ======================================================================================================
    def __init__(self, cap):
        # SYNTAX NOTE: 
        # - Snake case is preferred for general use due to its readability. 
        # - Camelcase is reserved for Booleans to help with comprehension.

        # define the VideoCapture object
        self.cap = cap

        # PARAMETERS: bg subtraction
        self.bg_sub_threshold = 30
        self.hist = 150
        self.bg_subtract = cv2.createBackgroundSubtractorMOG2(history=self.hist, varThreshold=self.bg_sub_threshold, detectShadows=False)

        # PARAMETERS: frame diff
        self.frame_diff_threshold = 100

        # PARAMETERS: contours
        self.min_contour_size = 5000

        # PARAMETERS: log files
        self.motion_logs_path = "./logs/motion_log.txt"
        self.object_logs_path = "./logs/object_log.txt"
        self.last_log_time = datetime.now() - timedelta(minutes=2) # make sure it starts writing at minute 0

        # PARAMETERS: object detection
        self.objectDetectionIsON = False
        self.obj_scan_duration = 30
        self.obj_scan_time_start = datetime.now()
        self.model = YOLO("yolov8n.pt")

        # PARAMETERS: Alert system
        isSendingAlerts = False
        user_alerter = emailAlert.emailAlertSystem()

    # MOTION ============================================================================================================
    def motion_object_scanner(self):
        
        while True:
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
            combined_frame = cv2.bitwise_or(frame_diff, foreground)
            _, combined_frame = cv2.threshold(combined_frame, self.frame_diff_threshold, 255, cv2.THRESH_BINARY)

            # contouring motion
            contours_array, _ = cv2.findContours(combined_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # OBJ DETECTION ====================================================================================================
            # if objectDetectionIsON, scan for objects. Otherwise, scan for motion 
            if self.objectDetectionIsON:
                
                # only run object detection model for 30 seconds
                elapsed_time = datetime.now() - self.obj_scan_time_start
                remaining_time = max(self.obj_scan_duration - elapsed_time.total_seconds(), 0)
                cv2.putText(frame, f"[Scanning for OBJECTS ({remaining_time:.0f}s)]", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
                
                if(elapsed_time > timedelta(seconds=self.obj_scan_duration)):
                    self.objectDetectionIsON = False
                    print(f"Switching to MOTION detection (self.objectDetectionIsON = False)")
                
                # TODO: do object detection here
                
            # MOTION DETECTION =================================================================================================
            else:
                cv2.putText(frame, "[Scanning for MOTION]", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                for c in contours_array:
                    size = cv2.contourArea(c)
                    if (size >= self.min_contour_size):
                        # uncomment below to draw motion boxes
                        #(x, y, w, h) = cv2.boundingRect(c)                    
                        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # add text top right corner
                        cv2.putText(frame, "[!] Motion Detected.", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                        
                        # write log
                        self.write_motion_logs()

                        # switch to OBJ DETECTION
                        self.objectDetectionIsON = True
                        self.obj_scan_time_start = datetime.now()
                        print(f"Switching to OBJ detection (self.objectDetectionIsON = True)")

            cv2.imshow("2A2S", frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
    # LOGS ====================================================================================================================================
    def get_curr_date_time(self):
        """Returns the current date and current time"""
        curr_time = datetime.now().strftime("%H:%M:%S")
        curr_date = date.today()
        return curr_date, curr_time

    def write_motion_logs(self):
        """Handles log writing when MOTION is detected"""
        
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

    def write_object_logs(self):
        # TODO: write function
        pass

    # USER ALERT SYSTEM ======================================================================================================================

def main():
    cap = cv2.VideoCapture(0)
    app = mySurveillanceClass(cap)
    app.motion_object_scanner()

    cap.release()
    cv2.destroyAllWindows() 

if __name__ == '__main__':
    main()
