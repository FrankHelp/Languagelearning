using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json; // Use Newtonsoft.Json
using System.Collections.Generic;

public class OpenAIChatGPT : MonoBehaviour
{
    private string apiKey = "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"; // Replace with an actual API key
    private string apiUrl = "https://api.openai.com/v1/chat/completions";

    public IEnumerator GetChatGPTResponse(List<ChatMessage> messages, System.Action<string> callback)
    {
        // Convert messages to API format
        var apiMessages = new List<object>();
        
        foreach (var msg in messages)
        {
            apiMessages.Add(new { role = msg.role, content = msg.content });
        }

        // Setting OpenAI API Request Data
        var jsonData = new
        {
            model = "gpt-4.1",
            messages = apiMessages.ToArray(),
            max_tokens = 500
        };

        string jsonString = JsonConvert.SerializeObject(jsonData);

        // HTTP request settings
        UnityWebRequest request = new UnityWebRequest(apiUrl, "POST");
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonString);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        request.SetRequestHeader("Authorization", "Bearer " + apiKey);

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
        {
            Debug.LogError("Error: " + request.error);
        }
        else
        {
            var responseText = request.downloadHandler.text;
            Debug.Log("Response: " + responseText);
            // Parse the JSON response to extract the required parts
            var response = JsonConvert.DeserializeObject<OpenAIResponse>(responseText);
            callback(response.choices[0].message.content.Trim());
        }
    }

    public class OpenAIResponse
    {
        public Choice[] choices { get; set; }
    }

    public class Choice
    {
        public Message message { get; set; }
    }

    public class Message
    {
        public string role { get; set; }
        public string content { get; set; }
    }
}