from engine import Engine, npTensor, rgbImage, lst
from modules import VideoReader, Display, recordReplayMultiplex, RRPlexMode
from pipeline.opticalflow import OpticalFlow

recordMode = RRPlexMode.BYPASS

shape = (960, 540)

# Initialize the engine with only the OpticalFlow module
engine = Engine(
    modules=[
        VideoReader(targetSize=shape),
        recordReplayMultiplex(OpticalFlow(), RRPlexMode.RECORD),
        Display(historyBufferSize=1000)
    ],
    signals={
        "image": rgbImage(shape[0], shape[1]),
        "opticalFlow": npTensor((2,)),
        "terminate": bool,
        "stopped": bool
    }
)

# Video data input
data = {"video": 'videos/1.mp4'}

# Run the engine and capture the signals
signals = engine.run(data)

# Print optical flow output (for verification)
print("Optical Flow Signals:", signals.get("opticalFlow", "No output"))

try:
    print("Press 'Esc' to exit the program gracefully.")
    signals = engine.run(data)

    # Monitor for exit command
    while True:
        # Check for keyboard input (wait for 1 ms to capture key press)
        if cv2.waitKey(1) == 27:  # 27 is the ASCII code for 'Esc'
            print("Exiting...")
            break

except KeyboardInterrupt:
    print("\nProgram interrupted. Exiting gracefully...")

finally:
    # Make sure to stop the engine and release resources
    engine.stop(data)
    print("Engine stopped and resources released.")