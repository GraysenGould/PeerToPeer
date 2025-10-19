import cv2
from vidgear.gears import CamGear
import time

# ----------------------------------------------------------------------
# Configuration: Point CamGear to the remote FastAPI stream URL.
# ----------------------------------------------------------------------
# You must adjust the IP/Port if your FastAPI server is running elsewhere.
REMOTE_STREAM_URL = "http://127.0.0.1:8000/video"

print(f"Connecting to remote stream at: {REMOTE_STREAM_URL}")

# Initialize CamGear with the remote URL. CamGear uses the network stream 
# capability of OpenCV's VideoCapture when a URL is provided.
try:
    stream = CamGear(source=REMOTE_STREAM_URL, logging=True).start()
    print("Connection established. Starting frame loop...")
except Exception as e:
    print(f"Error initializing CamGear with remote source: {e}")
    exit()


# Loop over frames and display them
while True:
    # This line remains the appropriate call, as the CamGear object 'stream' 
    # now abstracts the network reading instead of the local device reading.
    frame = stream.read() 
    
    if frame is None:
        # Stream has ended or failed to read (e.g., server disconnected)
        print("Stream ended or failed to read frame.")
        time.sleep(0.1)
        break
    
    cv2.imshow("Remote Video Stream (Press 'q' to exit)", frame)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
stream.stop()
print("Client shutdown complete.")
