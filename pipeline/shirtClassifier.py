import cv2
import numpy as np
from sklearn.cluster import KMeans


class ShirtClassifier:
    def __init__(self):
        self.name = "Shirt Classifier"
        self.teamAColor = (0, 0, 255)
        self.teamBColor = (255, 0, 0)

    def start(self, data):
        print("ShirtClassifier has started.")

    def stop(self, data):
        print("ShirtClassifier has stopped.")

    def step(self, data):
        image = data.get("image")
        tracks = data.get("tracks", [])
        track_classes = data.get("trackClasses", [])

        if image is None or len(tracks) == 0:
            return {
                "teamAColor": self.teamAColor,
                "teamBColor": self.teamBColor,
                "teamClasses": [0] * len(tracks),
            }
