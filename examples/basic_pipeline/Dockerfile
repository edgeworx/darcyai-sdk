FROM edgeworx/darcy-ai-base-x86:dev


WORKDIR /src

RUN python3 -m pip install darcyai-engine --upgrade

COPY . /src/

CMD python3 -u basic.py