from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import Response
import wave
# import whisper
from faster_whisper import WhisperModel
import os
import io
from pathlib import Path
import subprocess
import tempfile
# from piper import PiperVoice  # Korrekter Import

app = FastAPI()

PIPER_PATH = "./piper/piper.exe"
model_path = "./model/fr_FR-tom-medium.onnx"
model_path2 = "./model/de_DE-thorsten-high.onnx"

# model = whisper.load_model("small")  # Du kannst auch "small", "medium", etc. verwenden

model_size = "base"

# Run on CPU
model = WhisperModel(model_size, device="cpu", compute_type="int8")
# model = WhisperModel(model_size, device="cuda", compute_type="float16")
print("whispermodell geladen")


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

        # Temporäre Datei für Ausgabe
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_path = temp_wav.name

        try:
            # Piper aufrufen
            subprocess.run(
                [PIPER_PATH, "-m", model_path, "--length_scale", "0.9", "-f", temp_path],
                input=text.encode('utf-8'),
                check=True
            )
            
            # WAV-Daten lesen
            with open(temp_path, "rb") as f:
                wav_data = f.read()
            
            return Response(
                content=wav_data,
                media_type="audio/wav"
            )
            
        finally:
            # Temporäre Datei löschen
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except subprocess.CalledProcessError as e:
        print(f"Piper error: {e.stderr.decode()}")
        raise HTTPException(status_code=500, detail="Piper synthesis failed")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesizeDeutsch")
async def synthesize_text(request: Request):
    try:
        # Text aus dem Request-Body lesen
        text = (await request.body()).decode("utf-8").strip()
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        # Temporäre Datei für Ausgabe
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_path = temp_wav.name

        try:
            # Piper aufrufen
            subprocess.run(
                [PIPER_PATH, "-m", model_path2, "--length_scale", "0.9", "-f", temp_path],
                input=text.encode('utf-8'),
                check=True
            )
            
            # WAV-Daten lesen
            with open(temp_path, "rb") as f:
                wav_data = f.read()
            
            return Response(
                content=wav_data,
                media_type="audio/wav"
            )
            
        finally:
            # Temporäre Datei löschen
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except subprocess.CalledProcessError as e:
        print(f"Piper error: {e.stderr.decode()}")
        raise HTTPException(status_code=500, detail="Piper synthesis failed")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))