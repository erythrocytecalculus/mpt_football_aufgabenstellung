from engine import Engine, npTensor, rgbImage, lst
from modules import VideoReader, Display, recordReplayMultiplex, RRPlexMode
from pipeline.tracker import Tracker
import cv2

# Set the recording mode to BYPASS to directly use the Tracker
recordMode = RRPlexMode.BYPASS

# Define the video frame shape
shape = (960, 540)

# Initialize the engine with the Tracker module
engine = Engine(
    modules=[
        VideoReader(targetSize=shape),  # Video reading
        recordReplayMultiplex(Tracker(), RRPlexMode.BYPASS),  # Tracker module
        Display(historyBufferSize=1000)  # Visualization
    ],
    signals={
        "image": rgbImage(shape[0], shape[1]),  # Video frame
        "detections": npTensor((-1, 4)),  # Detected objects (x, y, w, h)
        "classes": npTensor((-1,)),  # Object classes (ball, player, goalkeeper, referee)
        "tracks": npTensor((-1, 4)),  # Tracked objects (x, y, w, h)
        "trackVelocities": npTensor((-1, 2)),  # Track velocities (vx, vy)
        "trackAge": lst(),  # Track age
        "trackClasses": lst(),  # Track classes
        "trackIds": lst(),  # Unique track IDs
        "terminate": bool,  # Exit signal
        "stopped": bool,  # Stop status
        "testout": int  # Test output
    }
)


# Define the video to be analyzed
data = {"video": 'videos/2.mp4'}

try:
    print("Running Tracker Module. Press 'Esc' to exit.")
    signals = engine.run(data)

    while True:
        # Check for key press to exit
        if cv2.waitKey(1) == 27:  # ASCII code for 'Esc'
            print("Exiting Tracker Module...")
            break

except KeyboardInterrupt:
    print("\nProgram interrupted. Exiting gracefully...")

print("Tracker Module stopped successfully.")
