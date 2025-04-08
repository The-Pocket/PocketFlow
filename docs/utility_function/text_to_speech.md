---
layout: default
title: "Text-to-Speech"
parent: "Utility Function"
nav_order: 7
---

# Text-to-Speech

| **Service**          | **Free Tier**         | **Pricing Model**                                            | **Docs**                                                            |
|----------------------|-----------------------|--------------------------------------------------------------|---------------------------------------------------------------------|
| **Amazon Polly**     | 5M std + 1M neural   | ~$4 /M (std), ~$16 /M (neural) after free tier               | [Polly Docs](https://aws.amazon.com/polly/)                         |
| **Google Cloud TTS** | 4M std + 1M WaveNet  | ~$4 /M (std), ~$16 /M (WaveNet) pay-as-you-go                | [Cloud TTS Docs](https://cloud.google.com/text-to-speech)           |
| **Azure TTS**        | 500K neural ongoing  | ~$15 /M (neural), discount at higher volumes                 | [Azure TTS Docs](https://azure.microsoft.com/products/cognitive-services/text-to-speech/) |
| **IBM Watson TTS**   | 10K chars Lite plan  | ~$0.02 /1K (i.e. ~$20 /M). Enterprise options available       | [IBM Watson Docs](https://www.ibm.com/cloud/watson-text-to-speech)   |
| **ElevenLabs**       | 10K chars monthly    | From ~$5/mo (30K chars) up to $330/mo (2M chars). Enterprise  | [ElevenLabs Docs](https://elevenlabs.io)                            |

## Example Python Code

### Amazon Polly
```python
import boto3

polly = boto3.client("polly", region_name="us-east-1",
                     aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
                     aws_secret_access_key="YOUR_AWS_SECRET_ACCESS_KEY")

resp = polly.synthesize_speech(
    Text="Hello from Polly!",
    OutputFormat="mp3",
    VoiceId="Joanna"
)

with open("polly.mp3", "wb") as f:
    f.write(resp["AudioStream"].read())
```

### Google Cloud TTS
```python
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
input_text = texttospeech.SynthesisInput(text="Hello from Google Cloud TTS!")
voice = texttospeech.VoiceSelectionParams(language_code="en-US")
audio_cfg = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

resp = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_cfg)

with open("gcloud_tts.mp3", "wb") as f:
    f.write(resp.audio_content)
```

### Azure TTS
```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="AZURE_KEY", region="AZURE_REGION")
audio_cfg = speechsdk.audio.AudioConfig(filename="azure_tts.wav")

synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_cfg
)

synthesizer.speak_text_async("Hello from Azure TTS!").get()
```

### IBM Watson TTS
```python
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

auth = IAMAuthenticator("IBM_API_KEY")
service = TextToSpeechV1(authenticator=auth)
service.set_service_url("IBM_SERVICE_URL")

resp = service.synthesize(
    "Hello from IBM Watson!",
    voice="en-US_AllisonV3Voice",
    accept="audio/mp3"
).get_result()

with open("ibm_tts.mp3", "wb") as f:
    f.write(resp.content)
```

### ElevenLabs
```python
import requests

api_key = "ELEVENLABS_KEY"
voice_id = "ELEVENLABS_VOICE"
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
headers = {"xi-api-key": api_key, "Content-Type": "application/json"}

json_data = {
    "text": "Hello from ElevenLabs!",
    "voice_settings": {"stability": 0.75, "similarity_boost": 0.75}
}

resp = requests.post(url, headers=headers, json=json_data)

with open("elevenlabs.mp3", "wb") as f:
    f.write(resp.content)
```

