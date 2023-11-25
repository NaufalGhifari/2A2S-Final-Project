""" 
    # train.py
    Training a model using a custom dataset. 
    Not linked to main.py, only used on its own for transfer learning a model.
"""
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model.train(data="<CUSTOM DATASET PATH HERE>", epochs=25, imgsz=640)