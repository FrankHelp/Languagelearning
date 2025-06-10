using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class TTSService : MonoBehaviour 
{
    public string serverUrl = "http://localhost:65432/synthesize";
    private AudioSource audioSource;

    void Start()
    {
        audioSource = gameObject.AddComponent<AudioSource>();
    }

    public void RequestTTS(string text) 
    {
        if (ContainsGermanWords(text))
        {
            StartCoroutine(PostTTSRequestDeutsch(text));
        }
        else
        {
            StartCoroutine(PostTTSRequest(text));
        }
    }

    private bool ContainsGermanWords(string text)
    {
        // Liste mit häufigen deutschen Wörtern zur Erkennung
        string[] germanWords = {
            "der", "die", "das", "und", "oder", "dich", "ist", "ich", "eine", "einer"
            // , "in", "zu", "den", "von", "mit", "sich",
            // "ist", "des", "im", "dem", "auch", "es", "an", "ich", "auf", "für",
            // "so", "eine", "als", "nach", "wie", "wir", "aus", "er", "hat", "dass",
            // "sie", "wird", "bei", "ein", "einen", "kann", "noch", "haben", "sind"
        };

        // Text in Kleinbuchstaben umwandeln für case-insensitive Suche
        string lowerText = text.ToLower();

        foreach (string word in germanWords)
        {
            // Prüfen, ob das Wort im Text vorkommt (mit Wortgrenzen)
            if (System.Text.RegularExpressions.Regex.IsMatch(lowerText, $@"\b{word}\b"))
            {
                return true;
            }
        }

        return false;
    }

    IEnumerator PostTTSRequest(string text) 
    {
        // Kein WWWForm verwenden - wir senden den Text direkt als Body
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(text);
        
        using (UnityWebRequest www = new UnityWebRequest(serverUrl, "POST"))
        {
            www.uploadHandler = new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = new DownloadHandlerAudioClip(serverUrl, AudioType.WAV);
            www.SetRequestHeader("Content-Type", "text/plain");

            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                
                if (audioSource != null)
                {
                    audioSource.clip = clip;
                    audioSource.Play();
                    Debug.Log("TTS Audio erfolgreich abgespielt");
                }
            }
            else
            {
                Debug.LogError("Fehler: " + www.error);
            }
        }
    }
    IEnumerator PostTTSRequestDeutsch(string text) 
    {
        // Kein WWWForm verwenden - wir senden den Text direkt als Body
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(text);
        
        using (UnityWebRequest www = new UnityWebRequest(serverUrl+"Deutsch", "POST"))
        {
            www.uploadHandler = new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = new DownloadHandlerAudioClip(serverUrl+"Deutsch", AudioType.WAV);
            www.SetRequestHeader("Content-Type", "text/plain");

            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                
                if (audioSource != null)
                {
                    audioSource.clip = clip;
                    audioSource.Play();
                    Debug.Log("TTS Audio erfolgreich abgespielt");
                }
            }
            else
            {
                Debug.LogError("Fehler: " + www.error);
            }
        }
    }
}