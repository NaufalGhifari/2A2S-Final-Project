# object detection =====================
from ultralytics import YOLO
import cv2 as cv
import supervision as sv

# gui ==================================
import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("2A2S GUI")

        self.label = tk.Label(self.master, text="2A2S Graphical User Interface (GUI)")
        self.label.pack()

        # test opencv cap
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
        self.update_cap()

    
    def update_cap(self):
        """
        1. Converts GRB to RGB
        2. Converts to tkinter image format
        3. Update the window
        """
        ret, frame = self.cap.read()

        if ret:
            rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # convert BGR to RGB

            img = Image.fromarray(rgb_image)
            img_tk = ImageTk.PhotoImage(img) # convert to tkinter image format

            # update tkinter label with the new image
            self.label.img = img_tk
            self.label.config(image=img_tk)

        # only update every 30 milisecs to improve performance
        self.master.after(30, self.update_cap)


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