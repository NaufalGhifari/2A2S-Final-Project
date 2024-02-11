# AI Augmented Surveillance System - 2A2S
Off the shelf webcam/CCTV surveillance system augmented with motion detection, object detection models, and email alert system.  
Final year project for BSc in Computer Science at University of London (AI & Machine Learning).

# 💡 2A2S Features
Features included in this project:  
- GUI
- Motion detection
- Object detection
  - Fire
  - Smoke
  - Intruder
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
- Other: sys, unittest, datetime

# 👷‍♂ To-Do:
- [x] Initialise project
- [x] Implement motion detection
- [x] Fine tune motion logs
- [x] Add timer function
- [ ] Train object detection models:
  - [ ] Fire
  - [ ] Smoke
  - [ ] Intruder
- [ ] Implement trained models
- [x] Implement logs for motion detection
- [ ] Implement logs for object detections
- [ ] Add save recording function
- [x] Email alert system for MOTION
- [ ] Email alert system for OBJECTS
- [ ] Implement GUI
  - [x] Start program button
  - [x] Minimum contour slider
  - [x] Object scan duration slider 

Author: Muhammad Naufal Al Ghifari
