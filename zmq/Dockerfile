FROM python:3.6.7-slim-stretch

RUN apt-get update && apt-get install -y make \
    gcc \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 && pip install -U pip

WORKDIR /zmq

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

VOLUME [ "/zmq" ]

EXPOSE 4444

CMD ["python", "zmqserver.py"]