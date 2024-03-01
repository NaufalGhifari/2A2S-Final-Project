import tkinter as tk
from tkinter import filedialog
from Detector import Detector_2A2S
import cv2
import threading
from PIL import Image, ImageTk
import subprocess
import os
import platform
from flask import Flask, render_template, send_from_directory, jsonify

class GUI_2A2S:
    def __init__(self, master):
        self.master = master
        self.master.title("2A2S Controls")
        self.master.geometry("1200x500")
        self.logs_path = "./logs/"
        self.operating_system = platform.system()

        # frame label (placeholder)
        self.frame_label = tk.Label(self.master, bg="black", text="2A2S: AI-Augmented Surveillance System\n\nPress \"Start Camera\" button to start video feed.\n(During first object scanning iteration, allow program ~15 seconds to boot up)", fg="white")
        self.frame_label.place(x=280, y=10, width=630, height=480)

        # start detector
        self.start_button = tk.Button(self.master, text="Start Camera", background="dodgerblue1", fg="azure2", font=("Helvetica", 11, "bold"), command=self.start_surveillance)
        self.start_button.place(x=15, y=10, width=250, height=125)

        # DASHBOARD ====================================================================================================================
        self.dashboard_thread = threading.Thread(target=self.start_dashboard())
        self.dashboard_thread.daemon = True
        self.dashboard_thread.start()

        # PARAMETER CONTROL ====================================================================================================================

        # object detection toggle
        self.set_objectDetectionIsON = False
        self.object_detection_button = tk.Button(self.master, text="Toggle Object Detection (OFF)", command=self.toggle_object_detection)
        self.object_detection_button.place(x=15, y=160, width=250, height=125)

        # Advanced parameters text
        self.text_adv_params = tk.Label(self.master, text="[!] Advanced Parameters [!]", font=("Arial", 14, "bold"))
        self.text_adv_params.place(x=930, y=35)

        # min contour slider
        self.text_min_contour = tk.Label(self.master, text="Minimum contour (0-10,000)")
        self.text_min_contour.place(x=930, y=100)
        self.slider_min_contour = tk.Scale(self.master, from_=10, to=1500, orient="horizontal", length=220, command=self.update_min_contour)
        self.slider_min_contour.set(500)
        self.slider_min_contour.place(x=930, y=120)

        # obj scan duration slider
        self.text_obj_scan_duration = tk.Label(self.master, text="Object scanning duration (30-300 seconds)")
        self.text_obj_scan_duration.place(x=930, y=200)
        self.slider_obj_scan_duration = tk.Scale(self.master, from_=30, to=300, orient="horizontal", length=220, command=self.update_obj_scan_duration)
        self.slider_obj_scan_duration.place(x=930, y=220)

        # frame differencing slider
        self.text_frame_diff_threshold = tk.Label(self.master, text="Frame differencing threshold (10-1,000)")
        self.text_frame_diff_threshold.place(x=930, y=300)
        self.slider_frame_diff_threshold = tk.Scale(self.master, from_=10, to=1000, orient="horizontal", length=220, command=self.update_frame_diff_threshold)
        self.slider_frame_diff_threshold.place(x=930, y=320)

        # background subtraction history slider
        self.text_bg_subtract_hist = tk.Label(self.master, text="Background subtraction history (5-1,000)")
        self.text_bg_subtract_hist.place(x=930, y=400)
        self.slider_bg_subtract_hist = tk.Scale(self.master, from_=5, to=1000, orient="horizontal", length=220, command=self.update_frame_diff_threshold)
        self.slider_bg_subtract_hist.set(150)
        self.slider_bg_subtract_hist.place(x=930, y=420)

        # open logs folder
        self.button_logs_folder = tk.Button(self.master, text="Open Logs Directory", command=self.open_logs_folder)
        self.button_logs_folder.place(x=15, y=310, width=250, height=125)

        # =======================================================================================================================================

        # quit application
        #self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_application, background="firebrick1", fg="azure2")
        #self.quit_button.place(x=15, y=600, width=200, height=100)

    def start_dashboard(self):
        """Runs dashboard, intended to be ran on a separate thread"""
        os.chdir("./Web_Dashboard")
        venv_path = "C:\PythonEnvs\CM3070_FinalProject\Scripts\python.exe"
        subprocess.run([venv_path, "dashboard.py"])

    def start_surveillance(self):
        cap = cv2.VideoCapture(0)
        self.Detector = Detector_2A2S(cap)
        
        # Run motion_object_scanner in a thread to make it non-blocking
        surveillance_thread = threading.Thread(target=self.Detector.motion_object_scanner)
        surveillance_thread.daemon = True  # terminate thread when main program exits
        surveillance_thread.start()

        self.update_frame()

    def update_frame(self):
        if hasattr (self, 'Detector'):
            frame = self.Detector.get_export_frame()
            if frame is not None:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(image=img)
                self.frame_label.imgtk = img
                self.frame_label.config(image=img)

        self.master.after(100, self.update_frame)

    def toggle_object_detection(self):
        """
        Toggles object detection model ON/OFF
        """
        # flip boolean
        self.set_objectDetectionIsON = not self.set_objectDetectionIsON

        # update button
        if self.set_objectDetectionIsON:
            self.object_detection_button.config(text="Toggle Object Detection (ON)")
        else:
            self.object_detection_button.config(text="Toggle Object Detection (OFF)")
        
        # update the parameter
        if self.Detector:
            self.Detector.objectDetectionIsON = self.set_objectDetectionIsON

    def update_min_contour(self, value):
        if hasattr (self, 'Detector'):
            value = int(value)
            if value <= 10000:
                self.Detector.min_contour_size = value

    def update_obj_scan_duration(self, value):
        if hasattr (self, 'Detector'):
            value = int(value)
            if 30 <= value <= 300:
                self.Detector.obj_scan_duration = value
    
    def update_frame_diff_threshold(self, value):
        if hasattr (self, 'Detector'):
            value = int(value)
            if 10 <= value <= 1000:
                self.Detector.frame_diff_threshold = value
    
    def update_bg_subtractor(self, value):
        if hasattr (self, 'Detector'):
            value = int(value)
            if 5 <= value <= 1000:
                self.Detector.hist = value
        
    def open_logs_folder(self):
        """
        Opens the directory that contains log information.
        Able to work on: Windows and Linux.
        Return: Void
        """
        
        # find the absolute path of the logs dir
        absolute_path = os.path.abspath(self.logs_path)
        
        # check OS and open accordingly
        if self.operating_system == "Windows":
            subprocess.Popen(['explorer', absolute_path])
        elif self.operating_system == "Linux":
            subprocess.Popen(['xdg-open', absolute_path])
        else:
            print("\nError while trying to open logs folder: Unsupported OS.\n")

    def quit_application(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = GUI_2A2S(root)
    root.mainloop()

if __name__ == "__main__":
    main()
