import cv2
import numpy as np
from sklearn.cluster import KMeans


class ShirtClassifier:
    def __init__(self):
        self.name = (
            "Shirt Classifier"  # Required module name for recording/replay system
        )
        self.teamAColor = (0, 0, 255)  # Default color for Team A (red in BGR)
        self.teamBColor = (255, 0, 0)  # Default color for Team B (blue in BGR)

    def start(self, data):
        # Initialization step when the module starts
        print("ShirtClassifier has started.")

    def stop(self, data):
        # Cleanup step when the module stops
        print("ShirtClassifier has stopped.")

    def step(self, data):
        # Extract the current frame and tracking data
        image = data.get("image")
        tracks = data.get("tracks", [])
        track_classes = data.get("trackClasses", [])  # Used to filter players only

        # If no image or no tracks available, return default results
        if image is None or len(tracks) == 0:
            return {
                "teamAColor": self.teamAColor,
                "teamBColor": self.teamBColor,
                "teamClasses": [0] * len(tracks),  # Assign 0 = undecided to all
            }

        player_colors = []  # Store average shirt color of each player
        player_ids = []  # Store track indices corresponding to players

        # Loop through each track and extract color if the class is "Player" (class ID = 2)
        for i, (bbox, cls) in enumerate(zip(tracks, track_classes)):
            if cls != 2:
                continue  # Skip non-player tracks

            x, y, w, h = bbox
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)

            # Focus on the upper half of the bounding box as the shirt region
            torso = image[y1 : y1 + int(0.5 * h), x1:x2]

            if torso.size == 0:
                continue  # Skip if cropped region is empty or invalid

            # Compute average color of the shirt area
            avg_color = np.mean(torso.reshape(-1, 3), axis=0)
            player_colors.append(avg_color)
            player_ids.append(i)

        # If not enough player samples, assign everyone as Team A by default
        if len(player_colors) < 2:
            return {
                "teamAColor": self.teamAColor,
                "teamBColor": self.teamBColor,
                "teamClasses": [0 if c != 2 else 1 for c in track_classes],
            }

        # Use KMeans clustering to split player shirt colors into two clusters (Team A and B)
        kmeans = KMeans(n_clusters=2, random_state=0)
        kmeans.fit(player_colors)
        centers = kmeans.cluster_centers_
        labels = kmeans.labels_

        # Assign the darker cluster as Team A for consistency
        if centers[0].mean() < centers[1].mean():
            self.teamAColor = tuple(map(int, centers[0]))
            self.teamBColor = tuple(map(int, centers[1]))
        else:
            self.teamAColor = tuple(map(int, centers[1]))
            self.teamBColor = tuple(map(int, centers[0]))
            labels = 1 - labels  # Flip labels to maintain Team A = darker color

        # Assign each track a team class based on clustering or original role
        team_classes = []
        for i in range(len(tracks)):
            if track_classes[i] != 2:
                team_classes.append(0)  # Not a player → undecided
            elif i in player_ids:
                idx = player_ids.index(i)
                team_classes.append(1 if labels[idx] == 0 else 2)
            else:
                team_classes.append(0)

        # Print colors for debugging
        print(f"Frame processed – Team A: {self.teamAColor}, Team B: {self.teamBColor}")

        # Return final team color info and classification for each track
        return {
            "teamAColor": self.teamAColor,
            "teamBColor": self.teamBColor,
            "teamClasses": team_classes,
        }
