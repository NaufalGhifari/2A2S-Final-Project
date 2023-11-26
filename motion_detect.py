"""
    # motion_detect.py
    Temporary file to develop motion detection feature
"""

import threading
import cv2 as cv
import imutils

cap = cv.VideoCapture(0)
self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv.COLOR_BGR2GRAY)
start_frame = cv.GaussianBlur(start_frame, (21, 21), 0)

alarmIsON = False
alarm_mode = False
alarm_counter = 0

def trigger_alarm():
    global alarm

    for _ in range(5):
        if not alarm_mode:
            break
        else:
            print("### ! ALARM TRIGGERED ! ###")
    
    alarmIsON = False

while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_bw = cv.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv.absdiff(frame_bw, start_frame)
        threshold = cv.threshold(difference, 25, 255, cv.THRESH_BINARY)[1]
        start_frame = frame

        # if theres movement above a certain value, increase alarm_counter
        if threshold.sum() > 300:
            alarm_counter += 1
        else:
            # reduce back to 0 if we dont see enough movement
            if alarm_counter > 0:
                alarm_counter -= 1

        cv.imshow("Cam", threshold)
    else:
        cv.imshow("Cam", frame)
    
    if alarm_counter > 20:
        alarmIsON = True
        threading.Thread(target=trigger_alarm).start()

    key_pressed = cv.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv.destroyAllWindows()