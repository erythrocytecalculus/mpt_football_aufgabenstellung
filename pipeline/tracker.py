import numpy as np
from scipy.optimize import linear_sum_assignment


class SimpleTrack:
    _next_id = 0

    def __init__(self, bbox, cls):
        self.id = SimpleTrack._next_id
        SimpleTrack._next_id += 1

        self.position = np.array(bbox, dtype=np.float32)
        self.previous_position = self.position.copy()
        self.velocity = np.zeros(2, dtype=np.float32)

        self.cls = cls
        self.age = 1
        self.missing = 0

    def predict(self):
        predicted = self.position.copy()
        predicted[0] += self.velocity[0]
        predicted[1] += self.velocity[1]
        self.previous_position = self.position
        self.position = predicted

    def update(self, bbox, cls):
        self.previous_position = self.position
        self.position = np.array(bbox, dtype=np.float32)
        self.velocity = self.position[:2] - self.previous_position[:2]
        self.cls = cls
        self.missing = 0
        self.age += 1

    def mark_missed(self):
        self.missing += 1
        self.age += 1
        self.predict()

    def should_remove(self, max_missing=5):
        return self.missing > max_missing


class Tracker:
    def __init__(self):
        self.name = "Tracker"
        self.tracks = []

    def start(self, data):
        self.tracks = []
        SimpleTrack._next_id = 0

    def stop(self, data):
        pass

    def _euclidean(self, p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def step(self, data):
        detections = np.asarray(data.get("detections", []), dtype=np.float32)
        det_classes = list(data.get("classes", []))

        max_dist = 250.0
        assigned = set()
        unmatched_tracks = list(range(len(self.tracks)))
        unmatched_dets = list(range(len(detections)))

        # Prediction step
        for t in self.tracks:
            t.predict()

        # Association via cost matrix
        if len(self.tracks) and len(detections):
            cost = np.zeros((len(self.tracks), len(detections)), dtype=np.float32)
            for i, track in enumerate(self.tracks):
                for j, det in enumerate(detections):
                    cost[i, j] = self._euclidean(track.position[:2], det[:2])
            row_ind, col_ind = linear_sum_assignment(cost)

            for r, c in zip(row_ind, col_ind):
                if cost[r, c] < max_dist:
                    self.tracks[r].update(detections[c], det_classes[c])
                    assigned.add((r, c))
                    unmatched_tracks.remove(r)
                    unmatched_dets.remove(c)

        # Update unmatched tracks
        for i in unmatched_tracks:
            self.tracks[i].mark_missed()

        # Create new tracks for unmatched detections
        for j in unmatched_dets:
            new_track = SimpleTrack(detections[j], det_classes[j])
            self.tracks.append(new_track)

        # Remove old tracks
        self.tracks = [t for t in self.tracks if not t.should_remove()]

        # Return required format
        return {
            "tracks": np.array([t.position for t in self.tracks], dtype=np.float32),
            "trackVelocities": np.array(
                [t.velocity for t in self.tracks], dtype=np.float32
            ),
            "trackAge": [t.age for t in self.tracks],
            "trackClasses": [t.cls for t in self.tracks],
            "trackIds": [t.id for t in self.tracks],
        }
