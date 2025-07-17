import io

import scipy.io.wavfile
import soundfile  # For converting MP3 bytes to NumPy array

from pocketflow import Node
from utils.audio_utils import play_audio_data, record_audio
from utils.call_llm import call_llm
from utils.speech_to_text import speech_to_text_api
from utils.text_to_speech import text_to_speech_api


class CaptureAudioNode(Node):
    """Records audio input from the user using VAD."""
    def exec(self, prep_res): # prep_res is not used as per design
        print("\nListening for your query...")
        audio_data, sample_rate = record_audio()
        if audio_data is None:
            return None, None
        return audio_data, sample_rate

    def post(self, shared, prep_res, exec_res):
        audio_numpy_array, sample_rate = exec_res
        if audio_numpy_array is None:
            shared["user_audio_data"] = None
            shared["user_audio_sample_rate"] = None
            print("CaptureAudioNode: Failed to capture audio.")
            return "end_conversation" 

        shared["user_audio_data"] = audio_numpy_array
        shared["user_audio_sample_rate"] = sample_rate
        print(f"Audio captured ({len(audio_numpy_array)/sample_rate:.2f}s), proceeding to STT.")

class SpeechToTextNode(Node):
    """Converts the recorded in-memory audio to text."""
    def prep(self, shared):
        user_audio_data = shared.get("user_audio_data")
        user_audio_sample_rate = shared.get("user_audio_sample_rate")
        if user_audio_data is None or user_audio_sample_rate is None:
            print("SpeechToTextNode: No audio data to process.")
            return None # Signal to skip exec
        return user_audio_data, user_audio_sample_rate

    def exec(self, prep_res):
        if prep_res is None:
            return None # Skip if no audio data

        audio_numpy_array, sample_rate = prep_res
        
        # Convert NumPy array to WAV bytes for the API
        byte_io = io.BytesIO()
        scipy.io.wavfile.write(byte_io, sample_rate, audio_numpy_array)
        wav_bytes = byte_io.getvalue()
        
        print("Converting speech to text...")
        transcribed_text = speech_to_text_api(audio_data=wav_bytes, sample_rate=sample_rate)
        return transcribed_text

    def post(self, shared, prep_res, exec_res):
        if exec_res is None:
            print("SpeechToTextNode: STT API returned no text.")
            return "end_conversation" 

        transcribed_text = exec_res
        print(f"User: {transcribed_text}")
        
        if "chat_history" not in shared:
            shared["chat_history"] = []
        shared["chat_history"].append({"role": "user", "content": transcribed_text})
        
        shared["user_audio_data"] = None
        shared["user_audio_sample_rate"] = None
        return "default"

class QueryLLMNode(Node):
    """Gets a response from the LLM."""
    def prep(self, shared):
        chat_history = shared.get("chat_history", [])
        
        if not chat_history:
            print("QueryLLMNode: Chat history is empty. Skipping LLM call.")
            return None 
        
        return chat_history

    def exec(self, prep_res):
        if prep_res is None: 
            return None 

        chat_history = prep_res
        print("Sending query to LLM...")
        llm_response_text = call_llm(messages=chat_history)
        return llm_response_text

    def post(self, shared, prep_res, exec_res):
        if exec_res is None:
            print("QueryLLMNode: LLM API returned no response.")
            return "end_conversation" 

        llm_response_text = exec_res
        print(f"LLM: {llm_response_text}")
        
        shared["chat_history"].append({"role": "assistant", "content": llm_response_text})
        return "default"

class TextToSpeechNode(Node):
    """Converts the LLM's text response into speech and plays it."""
    def prep(self, shared):
        chat_history = shared.get("chat_history", [])
        if not chat_history:
            print("TextToSpeechNode: Chat history is empty. No LLM response to synthesize.")
            return None
        
        last_message = chat_history[-1]
        if last_message.get("role") == "assistant" and last_message.get("content"):
            return last_message.get("content")
        else:
            print("TextToSpeechNode: Last message not from assistant or no content. Skipping TTS.")
            return None

    def exec(self, prep_res):
        if prep_res is None:
            return None, None
            
        llm_text_response = prep_res
        print("Converting LLM response to speech...")
        llm_audio_bytes, llm_sample_rate = text_to_speech_api(llm_text_response)
        return llm_audio_bytes, llm_sample_rate

    def post(self, shared, prep_res, exec_res):
        if exec_res is None or exec_res[0] is None:
            print("TextToSpeechNode: TTS failed or was skipped.")
            return "next_turn" 

        llm_audio_bytes, llm_sample_rate = exec_res
        
        print("Playing LLM response...")
        try:
            audio_segment, sr_from_file = soundfile.read(io.BytesIO(llm_audio_bytes))
            play_audio_data(audio_segment, sr_from_file)
        except Exception as e:
            print(f"Error playing TTS audio: {e}")
            return "next_turn" 

        if shared.get("continue_conversation", True):
            return "next_turn"
        else:
            print("Conversation ended by user flag.")
            return "end_conversation" 