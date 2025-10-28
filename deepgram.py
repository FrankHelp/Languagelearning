from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import Response
from fastapi import Form 
import wave
import os
import io
from pathlib import Path
from piper import PiperVoice
from piper.voice import SynthesisConfig
import time  # Neu hinzugefügt
import aiohttp
import json
import asyncio


app = FastAPI()

model_path_french = "./model/fr_FR-tom-medium.onnx"
model_path_german = "./model/de_DE-thorsten-high.onnx"
model_path_spanish = "/model/es_MX-claude-high.onnx"
model_path = "./model/fr_FR-tom-medium.onnx"
model_path2 = "./model/de_DE-thorsten-high.onnx"

spanish = False

tts_french = PiperVoice.load(model_path, use_cuda=False) # Cuda macht hier kaum was aus
tts_german = PiperVoice.load(model_path2, use_cuda=False)

# Deepgram API Key - sollte als Umgebungsvariable gesetzt werden
DEEPGRAM_API_KEY = ''

DEEPGRAM_API_URL = "https://api.deepgram.com/v1/listen"




async def transcribe_with_deepgram(audio_file_path: str, language: str = "fr") -> str:
    """
    Sendet eine Audiodatei an die Deepgram API zur Transkription
    """
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }
    
    # # Bestimme die Sprache für Deepgram
    # if spanish:
    #     deepgram_language = "es"
    # else:
    #     deepgram_language = "fr" if language == "fr" else "de"
    
    params = {
        "model": "nova-4",
        "language": f'{language}',
        "punctuate": "true",
        "numerals": "true"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            with open(audio_file_path, "rb") as audio_file:
                async with session.post(
                    DEEPGRAM_API_URL, 
                    headers=headers, 
                    params=params, 
                    data=audio_file
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status, 
                            detail=f"Deepgram API error: {error_text}"
                        )
                    
                    result = await response.json()
                    transcript = result.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
                    
                    return transcript.strip()
                    
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Temporäre Audiodatei speichern
        temp_audio = Path("temp_audio.wav")
        with open(temp_audio, "wb") as buffer:
            buffer.write(await file.read())
        
        print("Audio heruntergeladen! Starte Transkription mit Deepgram...")
        
        # Transkription mit Deepgram durchführen
        # language = "es" if spanish else "fr"
        # full_text = await transcribe_with_deepgram(str(temp_audio), language)
        full_text = await transcribe_with_deepgram(str(temp_audio), 'multi')
        
        print(f"Transkription: {full_text}")
        
        # Temporäre Datei löschen
        os.remove(temp_audio)
        
        return {"text": full_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribeMono")
async def transcribe_audio(file: UploadFile = File(...), lang: str = Form(...)): # lang-kürzel wie fr de en es
    try:
        # Temporäre Audiodatei speichern
        temp_audio = Path("temp_audio.wav")
        with open(temp_audio, "wb") as buffer:
            buffer.write(await file.read())
        print("Audio heruntergeladen! Starte Transkription mit Deepgram...")
        full_text = await transcribe_with_deepgram(str(temp_audio), lang)
        
        print(f"Transkription: {full_text}")
        
        # Temporäre Datei löschen
        os.remove(temp_audio)
        
        return {"text": full_text}
    except Exception as e:
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
