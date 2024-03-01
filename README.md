# AI Augmented Surveillance System - 2A2S
Off the shelf webcam/CCTV surveillance system augmented with motion detection, object detection models, and email alert system.  
Final year project for BSc in Computer Science at University of London (AI & Machine Learning).  

**Note**: This project is part of a final year university assignment. You are NOT to copy codes present in this repository whether it be in whole or in part for your own assignment; doing so would result in a violation of academic integrity in the form of plagiarism.

# 💡 2A2S Features
Features included in this project:  
- GUI
- Web application dashboard
- Motion detection
- Object detection using YoloV8
- Email alert system

## Workflow
![image](https://github.com/NaufalGhifari/2A2S-Final-Project/assets/85378958/3342d3cb-7e46-465d-b2ee-10f04d8b4d4e)

# 👨‍💻 How to get 2A2S running
1. Make sure you have [Python](https://www.python.org/downloads/) (version [3.10.7](https://www.python.org/downloads/release/python-3107/) is compatible)
2. Open cloned repo in the terminal.
3. Install all dependencies from [requirements.txt](https://github.com/NaufalGhifari/2A2S-Final-Project/blob/main/documentations/requirements.txt) with ```pip install -r /documentations/requirements.txt```.
4. Run the application with ```python gui.py```
5. You are using 2A2S!

# 🐍 Python packages
- [OpenCV](https://pypi.org/project/opencv-python/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Ultralytics](https://pypi.org/project/ultralytics/)
- [Supervision](https://pypi.org/project/supervision/)
- [PyTorch](https://pytorch.org/get-started/locally/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Threading](https://docs.python.org/3/library/threading.html)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- Other: sys, unittest, datetime, subprocess, etc.

# 👷‍♂ To-Do:
- [x] Initialise project
- [x] Implement motion detection
- [x] Fine tune motion logs
- [x] Add timer function
- [x] Implement trained models
- [x] Implement logs for motion detection
- [x] Add save snippet function
- [x] Email alert system for MOTION
- [x] Develop Dashboard web application
- [x] Integrate Dashboard to the rest of the system
- [x] Implement GUI
  - [x] Start program button
  - [x] Minimum contour slider
  - [x] Object scan duration slider
  - [x] Background subtraction history paramter slider
  - [x] Frame differencing threshold slider

# 👨‍🏫 Further improvements ideas
- [ ] Implement logs for object detections
- [ ] Email alert system for OBJECTS
- [ ] Train custom object detection models:
  - [ ] Fire
  - [ ] Smoke
  - [ ] Intruder

Author: Muhammad Naufal Al Ghifari
