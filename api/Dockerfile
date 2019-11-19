FROM python:3.6.7-slim-stretch

RUN apt-get update && apt-get install -y make \
    gcc \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 && pip install -U pip

WORKDIR /app

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

VOLUME [ "/app" ]

EXPOSE 8000

CMD ["python", "run.py"]