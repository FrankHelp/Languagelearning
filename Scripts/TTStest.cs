using UnityEngine;
using UnityEngine.UI;
using System.Net.Sockets;
using System.Text;
using System;
using Newtonsoft.Json;

public class TTStest : MonoBehaviour
    {
        [SerializeField] public TTSService synthesize;

        void Start()
        {
            // Button-Event hinzufügen
            synthesize.RequestTTS("Salut! Je suis votre Assistant au jour d'hui!");
        }
    }