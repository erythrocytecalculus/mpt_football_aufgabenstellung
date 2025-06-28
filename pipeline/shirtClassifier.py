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
        # TODO: Implement processing of a current frame list
        # The task of the shirt classifier module is to identify the two teams based on their shirt color and to assign each player to one of the two teams

        # Note: You can access data["image"] and data["tracks"] to receive the current image as well as the current track list
        # You must return a dictionary with the given fields:
        #       "teamAColor":       A 3-tuple (B, G, R) containing the blue, green and red channel values (between 0 and 255) for team A
        #       "teamBColor":       A 3-tuple (B, G, R) containing the blue, green and red channel values (between 0 and 255) for team B
        #       "teamClasses"       A list with an integer class for each track according to the following mapping:
        #           0: Team not decided or not a player (e.g. ball, goal keeper, referee)
        #           1: Player belongs to team A
        #           2: Player belongs to team B
        return {"teamAColor": None, "teamBColor": None, "teamClasses": None}
