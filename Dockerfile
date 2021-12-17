FROM edgeworx/darcy-ai-coral-armv7l:dev

COPY requirements.txt /src/
WORKDIR /src

RUN python3 -m pip install -r requirements.txt --upgrade

COPY perceptors/face_detector/ /src/

CMD python3 -u sample_pipeline.py
