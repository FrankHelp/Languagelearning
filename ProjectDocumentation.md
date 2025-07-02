# Documentation

26-06: I lost my saves of the documentation so far :(

Right now the python servers are running without the need for docker,

I've implemented structured outputs; the voice output is working and bilingual.



However the French and German Voice still is noticably different...

I've found matching "mls"? Voice IDs in the german and french mls packets, however they don't work really well with piper. I think they might have only been trained to pronounce the example sentence and get buggy when trying to create speech from sentences they don't know.



So goals today: 

- Run the TTS/Whisper Server on my Linux notebook (better processor) and access it from my macbook with unity (better mic quality)

- Add Function Calling for Saturation logic

- Outline possible Prompts for differing Language Levels A1-C2.



Okay, so running on different devices in the same network works but unity requires https connection and self signed certificates don't work.
