# Languagelearning ECA for Windows

Make sure to first download the newest version of Piper for Windows on
https://github.com/rhasspy/piper/releases/

#### Setup
First, unzip the downloaded piper_windows_amd64 file, and put the "piper" folder into
the root directory of the project (i.e. into Languagelearning ECA folder)

Then, setup your python environment:

You might need to input something like
$env:PATH = "C:\Users\2hammers\AppData\Local\Programs\Python\Python39;C:\Users\2hammers\AppData\Local\Programs\Python\Python39\Scripts;$env:PATH"
to enable python

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Once venv is activated, run:
pip install setuptools wheel
pip install -r requirements.txt

#### Running the Server

To start the server, run:
fastapi dev whisper_server_windows.py --port 65432

The port 65432 is important as it is hardcoded into unity c# scripts

#### Unity setup
At this point in time the unity setup is rudimentary. 
Just open a new 3D project, add a UI > Legacy > Button
*optional* Change the Button > Text to "Start Recording" in the inspector

Add the Scripts Folder from the git to your Project Assets folder
Drag and Drop "DialogueHandler.cs" and "WhisperTranscriber.cs" onto your Canvas Gameobject

Finally, link the Fields "Button" to the Button and the field "Transcriber" to WhisperTranscriber 
onto the Dialoguehandler.cs component in the canvas inspector.