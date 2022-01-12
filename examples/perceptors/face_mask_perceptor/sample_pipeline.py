import cv2
import numpy as np
import threading
from flask import Flask

from darcyai_engine.input.camera_stream import CameraStream
from darcyai_engine.output.live_feed_stream import LiveFeedStream
from darcyai_engine.pipeline import Pipeline

from face_mask_perceptor import FaceMaskPerceptor


class SamplePipeline():
    def __init__(self):
        camera = CameraStream(video_device="/dev/video0", fps=20)

        self.__flask_app = Flask(__name__)
        self.__pipeline = Pipeline(input_stream=camera,
                                   universal_rest_api=True,
                                   rest_api_flask_app=self.__flask_app,
                                   rest_api_base_path="/pipeline")

        live_feed = LiveFeedStream(
            flask_app=self.__flask_app, path="/live-stream")
        self.__pipeline.add_output_stream(
            "live_feed", self.__live_feed_callback, live_feed)

        face_mask_perceptor = FaceMaskPerceptor(threshold=0.9)
        self.__pipeline.add_perceptor("face_mask",
                                      face_mask_perceptor,
                                      input_callback=self.__mask_check_input_callback)

    def run(self):
        threading.Thread(
            target=self.__flask_app.run,
            kwargs={"host": "0.0.0.0", "port": 8080, "debug": False}).start()

        self.__pipeline.run()

    def __live_feed_callback(self, pom, input_data):
        frame = input_data.data.copy()

        color, label = ((0, 255, 0), "Mask") if pom.face_mask.has_mask() else ((0, 0, 255), "No Mask")
        cv2.rectangle(frame, (270, 180), (370, 300), color, 2)
        cv2.putText(frame, str(label), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        return frame

    def __mask_check_input_callback(self, input_data, pom, config):
        frame = input_data.data.copy()
        crop_face = frame[200:280, 280:360]
        color_cvt_face = cv2.cvtColor(crop_face, cv2.COLOR_BGR2RGB)

        return color_cvt_face


if __name__ == "__main__":
    sample_pipeline = SamplePipeline()
    sample_pipeline.run()
