FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg libgcc-s1 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install piper-tts
RUN pip install pydub


RUN pip install fastapi uvicorn python-multipart
RUN pip install faster-whisper


COPY . .

CMD ["uvicorn", "whisper_server:app", "--host", "0.0.0.0", "--port", "65432"]