import tkinter as tk
from Detector import Detector_2A2S
import cv2
import threading
from PIL import Image, ImageTk

class GUI_2A2S:
    def __init__(self, master):
        self.master = master
        self.master.title("2A2S Controls")
        self.master.geometry("1200x700")

        # create canvas
        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.place(x=280, y=0)

        # frame placeholder
        self.canvas.create_rectangle(0, 0, 630, 480, outline="black", fill="grey", width=2)
        self.canvas.create_text(315, 225, text="2A2S: AI-Augmented Surveillance System", fill="white")
        self.canvas.create_text(315, 250, text="Press \"Start Video\" button to start video feed.", fill="white")
        self.canvas.create_text(315, 275, text="(Allow ~15 seconds to boot up))", fill="white")

        # frame label
        self.frame_label = tk.Label(self.master, bg="grey")
        self.frame_label.pack()

        # start detector
        self.start_button = tk.Button(self.master, text="Start Video", command=self.start_surveillance)
        self.start_button.place(x=280, y=500)

        # PARAMETER CONTROL ====================================================================================================================

        # object detection toggle
        self.set_objectDetectionIsON = False
        self.object_detection_button = tk.Button(self.master, text="Toggle Object Detection: OFF", command=self.toggle_object_detection)
        self.object_detection_button.place(x=280, y=550)

        # min contour
        self.text_min_contour = tk.Label(self.master, text="Minimum contour (0-10,000)")
        self.text_min_contour.place(x=800, y=500)
        self.slider_min_contour = tk.Scale(self.master, from_=0, to=10000, orient="horizontal", length=200, command=self.update_min_contour)
        self.slider_min_contour.set(5000)
        self.slider_min_contour.place(x=800, y=520)

        # obj scan duration
        self.text_obj_scan_duration = tk.Label(self.master, text="Object scanning duration (30-300 seconds)")
        self.text_obj_scan_duration.place(x=800, y=600)
        self.slider_obj_scan_duration = tk.Scale(self.master, from_=30, to=300, orient="horizontal", length=200, command=self.update_obj_scan_duration)
        self.slider_obj_scan_duration.place(x=800, y=620)

        # =======================================================================================================================================

        # quit application
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_application, background="firebrick1", fg="azure2", width=10)
        self.quit_button.place(x=280, y=600)

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
            self.object_detection_button.config(text="Toggle Object Detection: ON")
        else:
            self.object_detection_button.config(text="Toggle Object Detection: OFF")
        
        # update the parameter
        if self.Detector:
            self.Detector.objectDetectionIsON = self.set_objectDetectionIsON

    def update_min_contour(self, value):
        value = int(value)
        if value <= 10000:
            self.Detector.min_contour_size = value

    def update_obj_scan_duration(self, value):
        value = int(value)
        if 30 <= value <= 300:
            self.Detector.obj_scan_duration = value

    def quit_application(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = GUI_2A2S(root)
    root.mainloop()

if __name__ == "__main__":
    main()
