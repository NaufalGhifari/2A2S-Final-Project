"""
    # gui.py
    handles the GUI part of the project
    CURRENTLY NOT IN USE
"""

import tkinter as tk
from PIL import Image, ImageTk
import cv2

class GUI:
    def __init__(self, root, cap):
        self.root = root
        self.root.minsize(800, 600) # set window minimal size
        self.root.title("2A2S GUI")

        # define an empty, then assign a cv2.VideoCapture input
        self.GUI_cap = None
        self.initialise_cap(cap)
        print("[DEBUG] GUI.GUI_cap.type() = ", type(self.GUI_cap))
        
        # canvas to display video feed
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        self.after_id = None

        self.update()

    def initialise_cap(self, new_cap):
        """Assigns new input to GUI_cap and resize"""
        self.GUI_cap = new_cap
        self.GUI_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.GUI_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        
    def update(self):
        success, frame = self.GUI_cap.read()
        if success:
            self.photo = self.convert_to_tk_image(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        self.after_id = self.root.after(30, self.update)

    def convert_to_tk_image(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        tk_image = ImageTk.PhotoImage(image=pil_image)
        return tk_image
    
    def change_video_source(self, new_cap):
        """Takes a cv2.VideoCapture() object"""

        # check if cap exists and release
        if hasattr(self, 'GUI_cap') and self.GUI_cap:
            self.GUI_cap.release()

        # Assign the new video input as self.GUI_cap
        self.initialise_cap(new_cap)

    def close(self):
        """
            Makes sure everything is closed & released to avoid crash
        """
        self.GUI_cap.release()
        self.root.destroy()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    root = tk.Tk()
    player = GUI(root, cap)

    root.protocol("WM_DELETE_WINDOW", player.close)
    root.mainloop()