import cv2
import numpy as np


class OpticalFlow:
    def __init__(self):
        self.name = "Optical Flow"  # Do not change the name of the module as otherwise recording replay would break!
        self.prev_gray = None
        self.scaling = 0.6  # Slight downscale for performance

    def start(self, data):
        print("[OpticalFlow] Module started.")
        self.prev_gray = None

    def stop(self, data):
        print("[OpticalFlow] Module stopped.")
        self.prev_gray = None

    def step(self, data):
        frame = data.get("image")
        if frame is None:
            return {"opticalFlow": np.array([0, 0], dtype=np.float32)}

        # Resize for faster processing
        if self.scaling < 1.0:
            frame = cv2.resize(frame, (0, 0), fx=self.scaling, fy=self.scaling)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # First frame - no flow
        if self.prev_gray is None:
            self.prev_gray = gray
            return {"opticalFlow": np.array([0, 0], dtype=np.float32)}

        # Calculate dense optical flow using Farneback
        flow = cv2.calcOpticalFlowFarneback(
            self.prev_gray,
            gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0,
        )

        # Compute average flow vector (x, y)
        avg_flow = np.mean(flow, axis=(0, 1))
        avg_flow = avg_flow.astype(np.float32) / self.scaling

        # Update previous frame
        self.prev_gray = gray

        return {"opticalFlow": avg_flow}
