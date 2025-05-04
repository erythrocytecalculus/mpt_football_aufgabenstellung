import cv2 as cv
import numpy as np

class ShirtClassifier:
    def __init__(self):
        self.name = "Shirt Classifier"  # Module name
        
        # Predefined histogram for Team A and Team B (these can be updated manually based on the teams' colors)
        self.teamA_histogram = None
        self.teamB_histogram = None
    
    def start(self, data):
        # Initialize anything needed at the start (e.g., team color histograms)
        pass
    
    def stop(self, data):
        # Any shutdown operations (if needed)
        pass
    
    def step(self, data):
        image = data["image"]  # Access the current frame
        tracks = data["tracks"]  # Access the tracks (bounding boxes of detected players)
        track_classes = data["trackClasses"]  # Access the classes for each tracked object

        teamAColor = None
        teamBColor = None
        teamClasses = []  # To store the team assignment for each player
        
        # Initialize histograms for Team A and Team B if not defined
        if self.teamA_histogram is None or self.teamB_histogram is None:
            # Define the reference histograms for Team A and Team B (These could be manually defined based on sample shirt colors)
            teamA_sample = cv.imread('teamA_sample_shirt.jpg')  # Sample image of Team A shirt
            teamB_sample = cv.imread('teamB_sample_shirt.jpg')  # Sample image of Team B shirt
            
            self.teamA_histogram = self.calculate_histogram(teamA_sample)
            self.teamB_histogram = self.calculate_histogram(teamB_sample)
        
        # Loop through all players and assign them to a team
        for index, track in enumerate(tracks):
            if track_classes[index] == 2:  # Only process players (class 2)
                x, y, w, h = track  # Extract bounding box for each player
                
                # Crop the player's shirt from the image using the bounding box
                shirt_crop = image[y:y+h, x:x+w]
                
                # Convert the shirt crop to HSV color space
                shirt_hsv = cv.cvtColor(shirt_crop, cv.COLOR_BGR2HSV)
                
                # Calculate the color histogram in the Hue channel
                shirt_hist = self.calculate_histogram(shirt_hsv)
                
                # Compare the histogram of the player's shirt to the predefined histograms for Team A and Team B
                dist_to_teamA = cv.compareHist(shirt_hist, self.teamA_histogram, cv.HISTCMP_CORREL)
                dist_to_teamB = cv.compareHist(shirt_hist, self.teamB_histogram, cv.HISTCMP_CORREL)
                
                # Assign the player to the closest team based on the histogram comparison
                if dist_to_teamA > dist_to_teamB:
                    teamClasses.append(1)  # Team A
                else:
                    teamClasses.append(2)  # Team B
        
        return {
            "teamAColor": teamAColor,
            "teamBColor": teamBColor,
            "teamClasses": teamClasses
        }

    def calculate_histogram(self, image):
        """Calculate a color histogram for the given image in the Hue channel"""
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        hist = cv.calcHist([hsv], [0], None, [256], [0, 256])  # Only use Hue channel (0th channel)
        cv.normalize(hist, hist, 0, 1, cv.NORM_MINMAX)  # Normalize the histogram
        return hist
