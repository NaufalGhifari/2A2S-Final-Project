"""
    # main.py 
    main file of the project
"""
import cv2
import motion_object_detect

#import gui
#import tkinter as tk
#import time

#from app import run_gui

def startMessage():
    print("\n+========================================+")
    print("| 2A2S: AI Augmented Surveillance System |")
    print("+========================================+\n")
    print("Loading, please wait...")

def main():
    #run_gui()
    
    cap = cv2.VideoCapture(0)

    # TODO: initialise GUI    

    # TODO: link motion detect w app 
    motion_sensor = motion_object_detect.Motion_Object_Detector(cap)
    motion_sensor.scanning_for_motion()

    # TODO: initialise object detection model

    # TODO: save snippet

    # TODO: alert email

    # TODO: display video in tk window (gui)
    
    

if (__name__ == "__main__"):
    startMessage()
    main()