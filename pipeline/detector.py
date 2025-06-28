from ultralytics import YOLO
import numpy as np


class Detector:
    def __init__(self, model_path="yolov8m-football.pt", conf_threshold=0.1):
        self.name = "Detector"
        self.model_path = model_path
        self.conf_threshold = conf_threshold

    def start(self, data):
        self.model = YOLO(self.model_path)
        print(f"Detector model '{self.model_path}' loaded.")

    def stop(self, data):
        print("Detector stopped.")

    def step(self, data):
        image = data["image"]
        results = self.model(image, verbose=False)
        boxes = results[0].boxes

        detections = []
        classes = []

        for box in boxes:
            cls_id = int(box.cls.item())
            conf = float(box.conf.item())

            if conf < self.conf_threshold:
                continue

            # Keep only Ball, Goalkeeper, Player, Referee
            if cls_id in [0, 1, 2, 3]:
                xywh = box.xywh[0].cpu().numpy()
                detections.append(xywh)
                classes.append(cls_id)

            else:
                continue

        if detections:
            detections = np.stack(detections)
            classes = np.array(classes, dtype=int)
        else:
            detections = np.zeros((0, 4))
            classes = np.zeros((0,), dtype=int)

        return {
            "detections": detections,  # shape: (N, 4)
            "classes": classes,  # shape: (N,)
        }
