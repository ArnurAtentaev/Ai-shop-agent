FROM python:3.13.2

WORKDIR /src

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY ./src .
COPY .env .
COPY ./language_detector.tflite .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
