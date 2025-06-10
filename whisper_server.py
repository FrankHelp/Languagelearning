from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import Response
import wave
# import whisper
from faster_whisper import WhisperModel
import os
import io
from pathlib import Path
from piper import PiperVoice  # Korrekter Import

app = FastAPI()

model_path = "/app/model/fr_FR-tom-medium.onnx"
model_path2 = "/app/model/de_DE-thorsten-high.onnx"

# model = whisper.load_model("small")  # Du kannst auch "small", "medium", etc. verwenden

model_size = "tiny"

# Run on CPU
model = WhisperModel(model_size, device="cpu", compute_type="int8")


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Temporäre Audiodatei speichern
        temp_audio = Path("temp_audio")
        with open(temp_audio, "wb") as buffer:
            buffer.write(await file.read())
        
        # Transkription durchführen
        # result = model.transcribe(str(temp_audio))
        # 
        print("audio runtergeladen!")
        segments, info = model.transcribe(str(temp_audio))
        result = list(segments)

        full_text = " ".join(segment.text for segment in result)

        print(full_text)
        
        # Temporäre Datei löschen
        os.remove(temp_audio)
        
        return {"text": full_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesize")
async def synthesize_text(request: Request):
    try:
        # Text aus dem Request-Body lesen
        text = (await request.body()).decode("utf-8").strip()
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        synthesize_args = {
            "length_scale": 1.2  # Wichtig: Verlangsamt die Sprechgeschwindigkeit
        }


        # Piper initialisieren
        tts = PiperVoice.load(model_path, use_cuda=False)

        # WAV-Daten im Speicher erstellen
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, "wb") as wav_file:
                tts.synthesize(text, wav_file, **synthesize_args)
            
            return Response(
                content=wav_io.getvalue(),
                media_type="audio/wav"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesizeDeutsch")
async def synthesize_text(request: Request):
    try:
        # Text aus dem Request-Body lesen
        text = (await request.body()).decode("utf-8").strip()
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")
        synthesize_args = {
            "length_scale": 0.9
        }


        # Piper initialisieren
        tts = PiperVoice.load(model_path2, use_cuda=False)

        # WAV-Daten im Speicher erstellen
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, "wb") as wav_file:
                tts.synthesize(text, wav_file, **synthesize_args)
            
            return Response(
                content=wav_io.getvalue(),
                media_type="audio/wav"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))