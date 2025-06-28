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

        player_colors = []
        player_ids = []

        for i, (bbox, cls) in enumerate(zip(tracks, track_classes)):
            if cls != 2:
                continue
            x, y, w, h = bbox
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)
            torso = image[y1 : y1 + int(0.5 * h), x1:x2]

            if torso.size == 0:
                continue

            avg_color = np.mean(torso.reshape(-1, 3), axis=0)
            player_colors.append(avg_color)
            player_ids.append(i)

        if len(player_colors) < 2:
            return {
                "teamAColor": self.teamAColor,
                "teamBColor": self.teamBColor,
                "teamClasses": [0 if c != 2 else 1 for c in track_classes],
            }

        kmeans = KMeans(n_clusters=2, random_state=0)
        kmeans.fit(player_colors)
        centers = kmeans.cluster_centers_
        labels = kmeans.labels_

        if centers[0].mean() < centers[1].mean():
            self.teamAColor = tuple(map(int, centers[0]))
            self.teamBColor = tuple(map(int, centers[1]))
        else:
            self.teamAColor = tuple(map(int, centers[1]))
            self.teamBColor = tuple(map(int, centers[0]))
            labels = 1 - labels
