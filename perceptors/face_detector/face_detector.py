import os
import pathlib
from typing import Any

from darcyai_coral.object_detection_perceptor import ObjectDetectionPerceptor
from darcyai_engine.config import Config
from darcyai_engine.config_registry import ConfigRegistry
from darcyai_engine.utils import validate_not_none, validate_type, validate


class FaceDetector(ObjectDetectionPerceptor):
    """
    Detect faces in an image.
    """

    def __init__(self, threshold:float=0.95):
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, "ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite")

        validate_not_none(threshold, "threshold is required")
        validate_type(threshold, (float, int), "threshold must be a number")
        validate(0 <= threshold <= 1, "threshold must be a number between 0 and 1")

        super().__init__(model_path=model_file,
                         threshold=0)

        self.config_schema = [
            Config("threshold", "float", threshold, "Threshold"),
        ]


    def run(self, input_data:Any, config:ConfigRegistry=None) -> Any:
        """
        This function is used to run the face detection.

        Arguments:
            input_data (Any): RGB array of the image.
            config (ConfigRegistry): The configuration.

        Returns:
            Any: The face detection result.
        """
        perception_result = super().run(input_data=input_data, config=config)

        result = []
        if len(perception_result) and len(perception_result[0]) > 0:
            for detection in perception_result[0]:
                if detection.id == 0 and detection.score >= config.threshold:
                    result.append(detection)

        return result
