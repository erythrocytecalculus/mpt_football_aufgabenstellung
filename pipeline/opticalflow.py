import numpy as np
import cv2

class OpticalFlow:
    def __init__(self):
        self.name = "Optical Flow"  # Keep the module name unchanged
        self.prev_frame = None  # Store the previous grayscale frame

    def start(self, data):
        # Initialize the previous frame as None
        self.prev_frame = None

    def stop(self, data):
        # Clean up resources if necessary
        self.prev_frame = None

    def step(self, data):
        # Access the current image from data
        image = data.get("image", None)

        # Return zero flow if no image is available
        if image is None:
            return {"opticalFlow": np.array([0, 0], dtype=np.float32)}

        # Convert the current image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # If this is the first frame, initialize prev_frame and return zero flow
        if self.prev_frame is None:
            self.prev_frame = gray
            return {"opticalFlow": np.array([0, 0], dtype=np.float32)}

        # Calculate optical flow using the Farneback method
        flow = cv2.calcOpticalFlowFarneback(
            self.prev_frame, gray, None, 
            0.5, 3, 15, 3, 5, 1.2, 0
        )

        # Compute the average flow in x and y directions
        flow_x = np.mean(flow[..., 0])
        flow_y = np.mean(flow[..., 1])

        # Update the previous frame
        self.prev_frame = gray

        # Return the calculated optical flow as a dictionary
        return {"opticalFlow": np.array([flow_x, flow_y], dtype=np.float32)}


