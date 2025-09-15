# LanguageLearning Backend Server
A Python FastAPI server providing speech-to-text (using OpenAI's Whisper) and text-to-speech (using Piper TTS) functionalities. This server acts as the python backend running local machine learning models for a Unity-based language learning prototype.


## Features
*   **Speech Synthesis French(TTS):** `/synthesize` endpoint - Converts text into speech (WAV audio) using Piper TTS and the tom-medium model.
*   **Speech Synthesis German(TTS):** `/synthesizeDeutsch` endpoint - Converts text into speech (WAV audio) using Piper TTS and the thorsten-high model.
*   **Speech Recognition (STT):** `/transcribe` endpoint - Converts speech (WAV audio) into text using Whisper, supporting Code-switching (FR/DE).

#### Setup

1.  **Prerequisites:** Ensure you have Python 3.8+ and `pip` installed.
2.  **Create a virtual environment** and activate it:
    ```bash
    python -m venv .venv
    ```
    **On Windows:**
    ```powershell
    .\.venv\Scripts\Activate.ps1
    # If you encounter execution policy issues, run:
    # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
    **On Linux/Mac:**
    ```bash
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Download voice models:**
    As Voice Models are too large for git (200MB) you have to download them manually:
    **On Linux/Mac:**
    ```bash
    curl -L -o model/de_DE-thorsten-high.onnx "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx?download=true"
    curl -L -o model/fr_FR-tom-medium.onnx "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx?download=true"
    ```
    **On Windows:**
    ```powershell
    curl.exe -L -o model/de_DE-thorsten-high.onnx "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx?download=true"
    curl.exe -L -o model/fr_FR-tom-medium.onnx "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx?download=true"
    
    ```
#### CUDA support

Code changes for CUDA support:
```python
tts_french = PiperVoice.load(model_path, use_cuda=True) # change to true 
tts_german = PiperVoice.load(model_path2, use_cuda=True) # change to true
```
```python
model = WhisperModel(model_size, device="cuda", compute_type="float16") # instead of device "cpu", compute_type="int8"
```

Note: The latest versions of ctranslate2 only support CUDA 12 and cuDNN 9. For CUDA 11 and cuDNN 8, the current workaround is downgrading to the 3.24.0 version of ctranslate2, for CUDA 12 and cuDNN 8, downgrade to the 4.4.0 version of ctranslate2, (This can be done with pip install --force-reinstall ctranslate2==4.4.0 or specifying the version in the requirements.txt).

#### Running the Server

To start the server in development mode with auto-reload (for code changes), run:
```bash
uvicorn whisper_server:app --host 0.0.0.0 --port 65432 --reload
```

#### API Usage

##### `POST /synthesize`
Synthesizes speech from the given text.
*   **Request Body:** Plain text string to be synthesized.
*   **Response:** A `audio/wav` file.

##### `POST /transcribe`
Transcribes speech from the given audio file.
*   **Request Form-Data:** A `file` parameter containing a WAV audio file.
*   **Response:** A JSON object with the transcribed text.
    ```json
    {"text": "Bonjour le monde"}
    ```
#### Test the server
You can test the server in a different terminal with curl:
**On Linux/Mac:**
```bash
curl -X POST --data "Bonjour le monde" http://localhost:65432/synthesize -o "bonjour.wav"
curl -X POST -F "file=@bonjour.wav" http://localhost:65432/transcribe
```
**On Windows:**
```bash
curl.exe -X POST --data "Bonjour le monde" http://localhost:65432/synthesize -o "bonjour.wav"
curl.exe -X POST -F "file=@bonjour.wav" http://localhost:65432/transcribe
```