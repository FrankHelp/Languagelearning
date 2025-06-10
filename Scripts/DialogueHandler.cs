using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections.Generic;
using UnityEngine.UI;

public class DialogueHandler : MonoBehaviour
{
    private List<ChatMessage> messages;
    [SerializeField] public Button recordingButton;

    private OpenAIChatGPT chatGPT;
    private TTSService tts;
    [SerializeField] public WhisperTranscriber _transcriber;

    private bool isRecording;
    private AudioClip recordedClip;

    private PromptHandler prompts;

    void OnEnable()
    {
        // Events abonnieren
        _transcriber.OnTranscriptionSuccess += HandleTranscriptionSuccess;
        _transcriber.OnTranscriptionError += HandleTranscriptionError;
    }

    void OnDisable()
    {
        // Events wieder abmelden (wichtig um Memory Leaks zu vermeiden!)
        _transcriber.OnTranscriptionSuccess -= HandleTranscriptionSuccess;
        _transcriber.OnTranscriptionError -= HandleTranscriptionError;
    }

    void Start()
    {
        tts = gameObject.AddComponent<TTSService>();
        chatGPT = gameObject.AddComponent<OpenAIChatGPT>();
        prompts = new PromptHandler();

        // Erstelle das Dictionary mit den Nachrichten
        messages = new List<ChatMessage>();

        recordingButton.onClick.AddListener(ToggleRecording);
        sendMessage(prompts.GetCurrentUserPrompt());
    }

    public void sendMessage(string userPrompt)
    {
        if(prompts.CheckForPromptSwitch())
        {
            messages.Add(new ChatMessage("system", prompts.GetCurrentSystemPrompt()));
            messages.Add(new ChatMessage("user", prompts.GetCurrentUserPrompt()));
            Debug.Log("Promptswitch!");
        }else
        {
            messages.Add(new ChatMessage("system", prompts.GetCurrentSystemPrompt()));
            messages.Add(new ChatMessage("user", userPrompt));
        }
        StartCoroutine(chatGPT.GetChatGPTResponse(messages, OnResponseReceived));
    }

    void OnResponseReceived(string response)
    {
        messages.Add(new ChatMessage("assistant", response));
        tts.RequestTTS(response);
        Debug.Log("ChatGPT Response: " + response);
    }

    void ToggleRecording()
    {
        if (!isRecording)
        {
            // Starte Aufnahme
            recordedClip = Microphone.Start(null, false, 60, 16000); // 60 Sekunden, 16 kHz
            recordingButton.GetComponentInChildren<Text>().text = "Stop Recording";
        }
        else
        {
            // Stoppe Aufnahme
            Microphone.End(null);

            // Konvertiere AudioClip in WAV-Daten
            byte[] wavData = ConvertAudioClipToWav(recordedClip);
            _transcriber.SendAudioRequest(wavData);

            recordingButton.GetComponentInChildren<Text>().text = "Start Recording";
        }
        isRecording = !isRecording;
    }

    byte[] ConvertAudioClipToWav(AudioClip clip)
    {
        return WavUtility.FromAudioClip(clip);
    }

    private void HandleTranscriptionSuccess(string result)
    {
        Debug.Log("Transkription erhalten: " + result);
        sendMessage(result);
    }

    // Event-Handler für Fehler
    private void HandleTranscriptionError(string error)
    {
        Debug.LogError("Transkription fehlgeschlagen: " + error);
        // Fehlerbehandlung (z. B. Fehlermeldung anzeigen)
    }
}