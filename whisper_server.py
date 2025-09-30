from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import Response
from fastapi import Form 
import wave
from faster_whisper import WhisperModel
import os
import io
from pathlib import Path
from piper import PiperVoice
from piper.voice import SynthesisConfig
import time  # Neu hinzugefügt

app = FastAPI()

model_path = "./model/fr_FR-tom-medium.onnx"
model_path2 = "./model/de_DE-thorsten-high.onnx"

tts_french = PiperVoice.load(model_path, use_cuda=True) # Cuda 
tts_german = PiperVoice.load(model_path2, use_cuda=True) # Cuda

model_size = "small"

# model = WhisperModel(model_size, device="cpu", compute_type="int8") # Ohne Cuda Beschleunigung ist Whisper 3-5 mal langsamer
model = WhisperModel(model_size, device="cuda", compute_type="float16") # Cuda

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    start_time = time.time()  # Startzeit messen
    
    try:
        temp_audio = Path("temp_audio")
        with open(temp_audio, "wb") as buffer:
            buffer.write(await file.read())
        
        print("audio runtergeladen!")
        segments, info = model.transcribe(str(temp_audio), initial_prompt="<|de|><|fr|><|transcribe|>")
        result = list(segments)

        full_text = " ".join(segment.text for segment in result)
        print(full_text)
        
        os.remove(temp_audio)
        
        # Gesamtzeit berechnen und ausgeben
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Transcribe Gesamtzeit: {total_time:.2f} Sekunden")
        
        return {"text": full_text}
    except Exception as e:
        # Auch bei Fehlern die Zeit messen
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Transcribe Fehlerzeit: {total_time:.2f} Sekunden")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribeMono")
async def transcribe_audio(file: UploadFile = File(...), lang: str = Form(...)): # lang-kürzel wie fr de en es
    start_time = time.time()  # Startzeit messen
    
    try:
        temp_audio = Path("temp_audio")
        with open(temp_audio, "wb") as buffer:
            buffer.write(await file.read())
        
        print("audio runtergeladen!")
        segments, info = model.transcribe(str(temp_audio), language=lang)
        result = list(segments)

        full_text = " ".join(segment.text for segment in result)
        print(full_text)
        
        os.remove(temp_audio)
        
        # Gesamtzeit berechnen und ausgeben
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Transcribe Gesamtzeit: {total_time:.2f} Sekunden")
        
        return {"text": full_text}
    except Exception as e:
        # Auch bei Fehlern die Zeit messen
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Transcribe Fehlerzeit: {total_time:.2f} Sekunden")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/synthesize")
async def synthesize_text(request: Request):
    start_time = time.time()  # Startzeit messen
    
    try:
        text = (await request.body()).decode("utf-8").strip()
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        config = SynthesisConfig(length_scale=1.2)
        
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, "wb") as wav_file:
                tts_french.synthesize_wav(text, wav_file, syn_config=config)
            
            # Gesamtzeit berechnen und ausgeben
            end_time = time.time()
            total_time = end_time - start_time
            print(f"Synthesize Gesamtzeit: {total_time:.2f} Sekunden")
            
            return Response(
                content=wav_io.getvalue(),
                media_type="audio/wav"
            )
    except Exception as e:
        # Auch bei Fehlern die Zeit messen
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Synthesize Fehlerzeit: {total_time:.2f} Sekunden")
        print(f"Fehler in synthesize: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesizeDeutsch")
async def synthesize_text(request: Request):
    start_time = time.time()  # Startzeit messen
    
    try:
        text = (await request.body()).decode("utf-8").strip()
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        config = SynthesisConfig(length_scale=0.9)

        with io.BytesIO() as wav_io:
            with wave.open(wav_io, "wb") as wav_file:
                tts_german.synthesize_wav(text, wav_file, syn_config=config)
            
            # Gesamtzeit berechnen und ausgeben
            end_time = time.time()
            total_time = end_time - start_time
            print(f"SynthesizeDeutsch Gesamtzeit: {total_time:.2f} Sekunden")
            
            return Response(
                content=wav_io.getvalue(),
                media_type="audio/wav"
            )
    except Exception as e:
        # Auch bei Fehlern die Zeit messen
        end_time = time.time()
        total_time = end_time - start_time
        print(f"SynthesizeDeutsch Fehlerzeit: {total_time:.2f} Sekunden")
        print(f"Fehler in synthesizeDeutsch: {e}")
        raise HTTPException(status_code=500, detail=str(e))
