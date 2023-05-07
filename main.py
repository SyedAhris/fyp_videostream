import os

from fastapi import FastAPI

from starlette.responses import StreamingResponse
from threading import Thread
import time

import cv2

from data import Data

app = FastAPI()

data = Data()


def read_file(video_dir):
    while True:
        cap = cv2.VideoCapture(video_dir)
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:

                # Display the resulting frame
                # cv2.imshow('Frame', frame)

                # convert frame to JPEG format
                _, encoded_frame = cv2.imencode('.jpg', frame)

                # convert JPEG-encoded frame to bytes
                bytes_frame = encoded_frame.tobytes()

                #split video_dir to get stream_id
                stream_id = video_dir.split('/')[-1].split('.')[0]
                # print(stream_id)
                data.data[stream_id] = bytes_frame
                # Press Q on keyboard to  exit
                # if cv2.waitKey(25) & 0xFF == ord('q'):
                #     break

            # Break the loop
            else:
                break

        # When everything done, release the video capture object
        cap.release()

for videos in os.listdir('./Videos'):
    video_dir = os.path.join('./Videos', videos)
    t = Thread(target=read_file, args=(video_dir, ))
    t.start()


def send_frame(stream_id: str):
    while True:
        frame_bytes = data.data[stream_id]
        # print(self.stream_frames[stream_name])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/{stream_id}')
async def stream_video(stream_id: str):
    return StreamingResponse(send_frame(stream_id),
                             media_type="multipart/x-mixed-replace; boundary=frame")
