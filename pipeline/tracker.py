# Note: A typical tracker design implements a dedicated filter class for keeping the individual state of each track
# The filter class represents the current state of the track (predicted position, size, velocity) as well as additional information (track age, class, missing updates, etc..)
# The filter class is also responsible for assigning a unique ID to each newly formed track
import numpy as np

class Filter:
    next_id = 1

    def __init__(self, z, cls):
        # Initialize the track state
        self.id = Filter.next_id
        Filter.next_id += 1
        self.position = np.array(z[:2], dtype=np.float32)  # (x, y) center
        self.size = np.array(z[2:4], dtype=np.float32)     # (width, height)
        self.velocity = np.array([0, 0], dtype=np.float32)  # Initial velocity
        self.age = 1                                       # Track age in frames
        self.class_id = int(cls)                           # Class of the tracked object
        self.missing_count = 0                             # Missing frame count

    def update(self, z):
        # Update the position and velocity of the track
        new_position = np.array(z[:2], dtype=np.float32)
        self.velocity = new_position - self.position  # Calculate velocity
        self.position = new_position
        self.size = np.array(z[2:4], dtype=np.float32)
        self.age += 1
        self.missing_count = 0  # Reset missing count

    def predict(self):
        # Predict the next position based on velocity
        self.position += self.velocity
        self.age += 1
        self.missing_count += 1

    def is_lost(self, max_missing=5):
        # Determine if the track should be removed
        return self.missing_count > max_missing

    def get_state(self):
        # Return the state vector (x, y, w, h)
        return np.concatenate((self.position, self.size))

class Tracker:
    def __init__(self):
        self.name = "Tracker"  # Keep the module name unchanged
        self.tracks = []       # List of current tracks

    def start(self, data):
        self.tracks = []

    def step(self, data):
        # Safely get detections and classes with a consistent shape
        detections = data.get("detections", np.empty((0, 4), dtype=np.float32))
        classes = data.get("classes", np.empty((0,), dtype=int))

        new_tracks = []
        track_states = []
        track_velocities = []
        track_ages = []
        track_classes = []
        track_ids = []
        team_classes = []

        # Update existing tracks with new detections
        for track in self.tracks:
            matched = False
            for i, detection in enumerate(detections):
                # Check if the detection has at least 4 elements
                if len(detection) < 4:
                    continue

                # Calculate distance between track and detection
                distance = np.linalg.norm(track.position - np.array(detection[:2]))

                # Check if the detection is close enough
                if distance < 50:
                    track.update(detection)
                    matched = True
                    # Remove used detection
                    detections = np.delete(detections, i, axis=0)
                    classes = np.delete(classes, i)
                    break

            # Predict position if no match is found
            if not matched:
                track.predict()

            # Keep track if it's not lost
            if not track.is_lost():
                new_tracks.append(track)
                track_states.append(track.get_state())
                track_velocities.append(track.velocity)
                track_ages.append(track.age)
                track_classes.append(track.class_id)
                track_ids.append(track.id)

                # Assign a default team class (0: undecided)
                team_classes.append(0)

        # Create new tracks for unmatched detections
        for detection, cls in zip(detections, classes):
            if len(detection) >= 4:
                new_track = Filter(detection, cls)
                new_tracks.append(new_track)
                track_states.append(new_track.get_state())
                track_velocities.append(new_track.velocity)
                track_ages.append(new_track.age)
                track_classes.append(cls)
                track_ids.append(new_track.id)

                # Default team class for new tracks
                team_classes.append(0)

        # Update tracks
        self.tracks = new_tracks

        # Convert to numpy arrays with consistent shape
        track_states = np.array(track_states, dtype=np.float32).reshape(-1, 4)
        track_velocities = np.array(track_velocities, dtype=np.float32).reshape(-1, 2)

        
        return {
            "tracks": np.array(track_states, dtype=np.float32).reshape(-1, 4),
            "trackVelocities": np.array(track_velocities, dtype=np.float32).reshape(-1, 2),
            "trackAge": track_ages,
            "trackClasses": track_classes,
            "trackIds": track_ids,
            "teamClasses": team_classes,
        }
    
    def stop(self, data):
        print("[Tracker] Module stopped.")
        



        
        
        
        
      
