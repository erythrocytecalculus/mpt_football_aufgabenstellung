from ultralytics import YOLO
import numpy as np


class Detector:
    def __init__(self, model_path="yolov8m-football.pt", conf_threshold=0.1):
        self.name = "Detector"
        self.model_path = model_path  # Path to the YOLO model weights
        self.conf_threshold = (
            conf_threshold  # Minimum confidence threshold for detections
        )

    def start(self, data):
        # Load the YOLO model from the given path when the module starts
        self.model = YOLO(self.model_path)
        print(f"Detector model '{self.model_path}' loaded.")

    def stop(self, data):
        # Optional cleanup when the module stops
        print("Detector stopped.")

    def step(self, data):
        # Extract the current video frame
        image = data["image"]

        # Run inference using the YOLO model
        results = self.model(image, verbose=False)
        boxes = results[0].boxes  # Get detected bounding boxes from the first result

        detections = []  # List to store bounding boxes
        classes = []  # List to store class IDs

        for box in boxes:
            cls_id = int(box.cls.item())  # Extract class ID
            conf = float(box.conf.item())  # Extract confidence score

            # Skip detections with low confidence
            if conf < self.conf_threshold:
                continue

            # Only include classes we care about: Ball (0), Goalkeeper (1), Player (2), Referee (3)
            if cls_id in [0, 1, 2, 3]:
                xywh = (
                    box.xywh[0].cpu().numpy()
                )  # Convert bounding box to (x_center, y_center, width, height)
                detections.append(xywh)
                classes.append(cls_id)

        # If detections were found, convert lists to numpy arrays
        if detections:
            detections = np.stack(detections)
            classes = np.array(classes, dtype=int)
        else:
            # Return empty arrays if no detections
            detections = np.zeros((0, 4))
            classes = np.zeros((0,), dtype=int)

        # Return detection data to the engine
        return {
            "detections": detections,  # Nx4 numpy array of (x_center, y_center, width, height)
            "classes": classes,  # N-length numpy array of class IDs
        }
