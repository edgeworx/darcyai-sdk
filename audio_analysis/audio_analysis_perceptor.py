import numpy as np
import os
import pathlib
import tflite_runtime.interpreter as tflite

from darcyai_engine.perceptor.perceptor import Perceptor
from darcyai_engine.config import Config


class AudioAnalysisPerceptor(Perceptor):
    """
    AudioAnalysisPerceptor is a Perceptor that can be used to analyze audio data.
    """
    def __init__(self):
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, "sound_edgetpu.tflite")
        labels_file = os.path.join(script_dir, "labels.txt")

        super().__init__(model_path=model_file)

        self.__interpreter = None
        with open(labels_file) as file:
            lines = file.readlines()
            self.__sound_names = [line.rstrip() for line in lines]

    def run(self, input_data, config):
        """
        Run the audio analysis perceptor.

        # Arguments
        input_data (np.array): The input data to the perceptor.
            This is expected to be a [1, 193] float32 numpy array.
        config (Config): The configuration for the perceptor.
        """
        self.__interpreter.set_tensor(self.__input_details[0]['index'], input_data)
        self.__interpreter.invoke()
        tflite_model_predictions = self.__interpreter.get_tensor(self.__output_details[0]['index'])

        ind = np.argpartition(tflite_model_predictions[0], -2)[-2:]
        ind[np.argsort(tflite_model_predictions[0][ind])]
        ind = ind[::-1]
        top_certainty = int(tflite_model_predictions[0, ind[0]] * 100)
        second_certainty = int(tflite_model_predictions[0, ind[1]] * 100)
        if top_certainty > 60:
            print(f"Top guess: {self.__sound_names[ind[0]]} ({top_certainty}%)")
            print(f"Second guess: {self.__sound_names[ind[1]]} ({second_certainty}%)")

    def load(self, accelerator_idx=None):
        """
        Load the audio analysis perceptor.

        # Arguments
        accelerator_idx (int): The index of the Edge TPU accelerator to use.
        """
        self.__interpreter = tflite.Interpreter(model_path=self.model_path, experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        self.__input_details = self.__interpreter.get_input_details()
        self.__output_details = self.__interpreter.get_output_details()

        self.__interpreter.allocate_tensors()

        super().set_loaded(True)
