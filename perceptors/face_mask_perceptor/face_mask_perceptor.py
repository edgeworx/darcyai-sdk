import os
import pathlib
from typing import Any

from darcyai_coral.image_classification_perceptor import ImageClassificationPerceptor
from darcyai_engine.config import Config
from darcyai_engine.config_registry import ConfigRegistry
from darcyai_engine.utils import validate_not_none, validate_type, validate
from face_mask_detection_model import FaceMaskDetectionModel


class FaceMaskPerceptor(ImageClassificationPerceptor):
    """
    This class is a subclass of ImageClassificationPerceptor.
    It is used to detect face mask in an image.
    """

    def __init__(self, threshold:float=0.95):
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, "face_mask_detection.tflite")

        labels = {
            0: "No Mask",
            1: "Mask",
        }

        validate_not_none(threshold, "threshold is required")
        validate_type(threshold, (float, int), "threshold must be a number")
        validate(0 <= threshold <= 1, "threshold must be a number between 0 and 1")

        super().__init__(model_path=model_file,
                         threshold=0,
                         top_k=2,
                         labels=labels)

        self.config_schema = [
            Config("threshold", "float", threshold, "Threshold"),
        ]


    def run(self, input_data:Any, config:ConfigRegistry=None) -> FaceMaskDetectionModel:
        """
        This function is used to run the face mask detection.

        Arguments:
            input_data (Any): RGB array of the face.
            config (ConfigRegistry): The configuration.

        Returns:
            FaceMaskDetectionModel: The face mask detection model.
        """
        perception_result = super().run(input_data=input_data, config=config)

        if len(perception_result[1]) == 0:
            has_mask = False
        else:
            idx = perception_result[1].index("Mask")
            has_mask = perception_result[0][idx][1] >= self.get_config_value("threshold")

        return FaceMaskDetectionModel(has_mask)
