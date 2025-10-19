from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from vidgear.gears import CamGear
import cv2

app = FastAPI()
stream = CamGear(source=0).start()

def generate():
    while True:
        frame = stream.read()
        if frame is None:
            break   
        _, jpeg = cv2.imencode(".jpg", frame)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n")


@app.get("/video")
def video_feed():
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")


#run: python -m uvicorn main:app --host 0.0.0.0 --port 8000
#ngrok http 8000 --url https://default.internal