"""
    # app.py
    Handles the GUI part of the project
"""

# object detection =====================
from ultralytics import YOLO
import cv2 as cv
import supervision as sv
import torch
import time

# gui ==================================
import tkinter as tk
from PIL import Image, ImageTk

class App:
    """

    """
    def __init__(self, master):
        """

        """
        self.master = master
        self.master.title("2A2S GUI")
        
        self.scan_duration = 5
        self.object_scanning = False
        self.detecting_motion = False

        # load model
        try:
            model_path = 'yolov8n.pt'
            self.model = YOLO(model_path)
        except IOError as err:
            print("[!] Error occured while loading model: ", err)
            return
        
        # use GPU if available
        if(self.gpu_check() == True):
            print("Switching to GPU...")
            self.model.to('cuda')
            
        self.label = tk.Label(self.master, text="2A2S Graphical User Interface (GUI)")
        self.label.pack()

        # capture video feed
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

        # setup supervision BoxAnnotator
        self.boxAnnotator = sv.BoxAnnotator(
            thickness = 2,
            text_thickness = 2,
            text_scale = 1
        )

        # update the video in the GUI
        self.update_cap()

    def gpu_check(self):
        """Checks if a GPU is available. Returns boolean."""
        if torch.cuda.is_available():
            print("CUDA (GPU) is available. Version: ", torch.version.cuda)
            return True
        else:
            print("CUDA (GPU) is not available. Using CPU.")
            return False
    
    def update_cap(self):
        """
            1. Converts GRB to RGB
            2. Converts to tkinter image format
            3. Update the window
        """
        success, img = self.cap.read()

        if success:
    # ==============================================================
    # TODO: performance is still bad
            
            self.motion_detected()
            if (self.detecting_motion):
                print("## Motion detected! ##")

                results = self.model(img)[0]
                detections = sv.Detections.from_ultralytics(results)

                scan_start_time = time.time() # get current time
                self.scan_for_objects(img, detections, scan_start_time)
                
    def scan_for_objects(self, img, detections, scan_start_time):

        if time.time() - scan_start_time < self.scan_duration:
            # annotate images
            img = self.boxAnnotator.annotate(
                scene=img,
                detections=detections
            )

            # make img compatible with tk
            img_tk = self.cv_cap_to_tkinter_image(img)

            # update tkinter label with the new image
            self.label.img = img_tk
            self.label.config(image=img_tk)

            # only update every 30 milisecs to improve performance
            self.master.after(100, self.update_cap)
        else:
            self.detecting_motion = False
            self.master.after(30, self.update_cap)

    # ==============================================================
    def cv_cap_to_tkinter_image(self, input):
        """
            cv2 VideoCapture stores video as a numpy array, this is not compatible with tkinter.  
            Use PIL to convert it into a tkinter compatible image.
            1. Convert BGR to RGB 
            2. Convert array to Image class
            3. Convert Image to tk compatible image
        """
        # convert BGR to RGB
        rgb_image = cv.cvtColor(input, cv.COLOR_BGR2RGB) 
        
        # convert to tkinter image format
        pil_img = Image.fromarray(rgb_image)
        tkinter_img = ImageTk.PhotoImage(pil_img) 
        
        return tkinter_img

    
    def motion_detected(self): # [WIP]
        """Compare current frame with the previous frame to detect motion. Returns boolean."""

        ret, prev_frame = self.cap.read() # get previous frame

        while True:
            ret, curr_frame = self.cap.read() # get current frame

            # reduce dimensions to imrpove perf
            prev_frame_gray = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
            curr_frame_gray = cv.cvtColor(curr_frame, cv.COLOR_BGR2GRAY)

            # calc difference between the two
            difference = cv.absdiff(prev_frame_gray, curr_frame_gray)

            # =========================================================================================
            # TODO: REFACTOR
            # Apply a threshold to highlight regions with significant differences
            _, thresholded_diff = cv.threshold(difference, 30, 255, cv.THRESH_BINARY)
            
            # Find contours in the thresholded difference image
            contours, _ = cv.findContours(thresholded_diff, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # Check if contours (motion) are detected
            motion_detected = len(contours) > 0 
            # =========================================================================================

            # Break the loop if motion is detected
            if motion_detected:
                break

            #video_input.release()

        self.detecting_motion = True











    def close(self):
        """
            Makes sure everything is closed & released to avoid crash
        """
        self.cap.release()
        self.master.destroy()
    
def run_gui():
    root = tk.Tk()
    root.minsize(800, 600) # set window minimal size
    
    app = App(root)
    root.mainloop()