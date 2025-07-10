import numpy as np

class Filter:
    _next_id = 1  # static class variable to assign unique IDs to each filter instance

    def __init__(self, z, cls):
        # Initialize state vector with 6 elements: [x, y, w, h, vx, vy]
        self.x = np.zeros((6,), dtype=np.float32)
        self.x[:4] = z  # set initial position and size based on detection
        self.cls = int(cls)  # object class

        # Initial state covariance matrix (P): higher uncertainty in velocity
        self.P = np.diag([10, 10, 10, 10, 1000, 1000]).astype(np.float32)

        # State transition matrix (F): assumes constant velocity model
        self.F = np.eye(6, dtype=np.float32)
        self.F[0, 4] = 1.0  # x += vx
        self.F[1, 5] = 1.0  # y += vy

        # Observation matrix (H): only measures position and size (4D)
        self.H = np.zeros((4, 6), dtype=np.float32)
        self.H[0, 0] = self.H[1, 1] = self.H[2, 2] = self.H[3, 3] = 1.0

        # Process noise (Q) and measurement noise (R)
        self.Q = np.eye(6, dtype=np.float32) * 0.01
        self.R = np.eye(4, dtype=np.float32) * 1.0

        self.id = Filter._next_id  # assign unique ID
        Filter._next_id += 1

        self.age = 1       # track age in frames
        self.misses = 0    # count of consecutive missed detections

    def predict(self):
        self.x = self.F @ self.x  # predict next state
        self.P = self.F @ self.P @ self.F.T + self.Q  # update covariance
        self.age += 1
        self.misses += 1  # increase missed count

    def update(self, z):
        z = np.asarray(z, dtype=np.float32)
        y = z - self.H @ self.x  # innovation
        S = self.H @ self.P @ self.H.T + self.R  # innovation covariance
        K = self.P @ self.H.T @ np.linalg.inv(S)  # Kalman gain
        self.x = self.x + K @ y  # update state
        I = np.eye(6, dtype=np.float32)
        self.P = (I - K @ self.H) @ self.P  # update covariance
        self.misses = 0  # reset misses on successful update

    def get_state(self):
        return self.x[:4].copy()  # return position and size (x, y, w, h)

    def get_velocity(self):
        return self.x[4:].copy()  # return velocity (vx, vy)

    def is_deleted(self, max_misses=5):
        return self.misses >= max_misses  # delete if too many misses


class Tracker:
    def __init__(self):
        self.name = "Tracker"
        self.filters = []  # list of active tracks
        self.max_misses = 5  # allowed misses before deleting a track
        self.dist_thresh = 50.0  # max Euclidean distance for matching
        self.frame_count = 0

    def start(self, data):
        print("[Tracker] Tracking started.")
        self.filters = []  # clear filters
        Filter._next_id = 1  # reset ID counter
        self.frame_count = 0

    def stop(self, data):
        print("[Tracker] Tracking stopped.")
        self.filters = []

    def step(self, data):
        self.frame_count += 1
        dets = np.asarray(data.get("detections", []), dtype=np.float32)
        classes = list(data.get("classes", []))

        # Prediction step for all filters
        for f in self.filters:
            f.predict()

        unmatched_dets = list(range(len(dets)))

        # Matching detections to existing filters based on Euclidean distance
        for f in self.filters:
            best_idx = -1
            best_dist = float("inf")
            for i in unmatched_dets:
                dist = np.linalg.norm(f.get_state()[:2] - dets[i][:2])
                if dist < best_dist and dist < self.dist_thresh:
                    best_idx = i
                    best_dist = dist
            if best_idx >= 0:
                f.update(dets[best_idx])
                f.cls = classes[best_idx]
                unmatched_dets.remove(best_idx)

        # Create new filters for unmatched detections
        for i in unmatched_dets:
            nf = Filter(dets[i], classes[i])
            self.filters.append(nf)

        # Remove filters that have been missed too often
        self.filters = [f for f in self.filters if not f.is_deleted(self.max_misses)]

        # Prepare tracking result
        result = {
            "tracks": np.array([f.get_state() for f in self.filters], dtype=np.float32),
            "trackVelocities": np.array(
                [f.get_velocity() for f in self.filters], dtype=np.float32
            ),
            "trackAge": [f.age for f in self.filters],
            "trackClasses": [f.cls for f in self.filters],
            "trackIds": [f.id for f in self.filters],
        }

        # Print tracking result for debug
        print(f"\n--- Frame {self.frame_count} ---")
        print("Tracks:", result["tracks"])
        print("Velocities:", result["trackVelocities"])
        print("Ages:", result["trackAge"])
        print("Classes:", result["trackClasses"])
        print("IDs:", result["trackIds"])

        return result
