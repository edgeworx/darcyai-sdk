import time
from darcyai_engine.input.input_stream import InputStream
from darcyai_engine.stream_data import StreamData
from darcyai_engine.utils import timestamp

class SampleInputStream(InputStream):
    def __init__(self,):
        self.__stopped = True


    def stop(self):
        self.__stopped = True


    def stream(self):
        self.__stopped = False

        while not self.__stopped:
            time.sleep(1)

            yield(StreamData("Hello!", timestamp()))
