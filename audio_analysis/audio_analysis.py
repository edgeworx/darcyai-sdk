import librosa
import numpy as np
from flask import Flask

from darcyai_engine.pipeline import Pipeline

from audio_input_stream import AudioInputStream
from audio_analysis_perceptor import AudioAnalysisPerceptor

class AudioAnalyzer():
    def __init__(self):
        mic = AudioInputStream(sample_len_sec=1)
        self.__rate = mic.get_sample_rate()

        self.__pipeline = Pipeline(input_stream=mic)

        audio_perceptor = AudioAnalysisPerceptor()
        self.__pipeline.add_perceptor("audio_analyzer",
                                      audio_perceptor,
                                      input_callback=self.__audio_perceptor_input_callback)

    def run(self):
        self.__pipeline.run()

    def __audio_perceptor_input_callback(self, input_data, pom, config):
        data = np.frombuffer(input_data.data, dtype=np.float32)
        return data[:193]
        return self.__extract_features(data)

    def __extract_features(self, data):
        features = np.empty((0, 193))

        stft = np.abs(librosa.stft(data))
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=self.__rate, n_mfcc=40).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=self.__rate).T, axis=0)
        mel = np.mean(librosa.feature.melspectrogram(data, sr=self.__rate).T, axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=self.__rate).T, axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(data), sr=self.__rate).T, axis=0)
        ext_features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
        features = np.vstack([features, ext_features]).astype(np.float32)

        return features

if __name__ == "__main__":
    audio_analyzer = AudioAnalyzer()
    audio_analyzer.run()
