from ultralytics import YOLO


class Detector:
    def __init__(self):
        self.name = "Detector"
        # Load the custom-trained YOLOv8 model (use the correct path to your .pt file)
        self.model = YOLO(
            "path/to/yolov8m-football.pt"
        )  # Replace with the correct path

    def start(self, data):
        # Initialize any variables or settings needed at the start
        pass

    def stop(self, data):
        # Perform any shutdown operations (if needed)
        pass

    def step(self, data):
        image = data["image"]  # Access the current frame from the data

        # Run inference using the YOLOv8 model
        results = self.model(image)  # Perform inference

        # Get the bounding boxes (xywh format: x_center, y_center, width, height)
        detections = results.xywh[0].cpu().numpy()  # Extract detections
        class_names = results.names  # List of class names (ball, player, etc.)

        # Set a confidence threshold for filtering out low-confidence detections
        confidence_threshold = 0.5
        detections = detections[
            detections[:, 4] > confidence_threshold
        ]  # Keep only detections with confidence > 0.5

        class_ids = detections[:, -1].astype(
            int
        )  # Get the class IDs of the detected objects

        # Prepare bounding boxes and class labels
        boxes = detections[:, :4]  # Bounding boxes (x_center, y_center, width, height)
        class_labels = [
            class_names[class_id] for class_id in class_ids
        ]  # Get the class labels for each detection

        # Return detections and class labels
        return {
            "detections": boxes,  # Bounding box coordinates (X, Y, W, H)
            "classes": class_labels,  # Corresponding class labels (ball, player, goalkeeper, referee)
        }
