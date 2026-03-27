from pocketflow import Node
from utils import call_llm, text_to_speech, DOCS
import yaml
import wave
import os


VOICES = {"Alex": "alloy", "Jamie": "echo"}


class AnalyzeDocs(Node):
    def prep(self, shared):
        """Read documents from the shared store."""
        return shared.get("docs", DOCS)

    def exec(self, docs):
        """Extract interesting nuggets from each document."""
        all_docs = "\n\n---\n\n".join(
            f"Document {i+1}:\n{doc}" for i, doc in enumerate(docs)
        )
        prompt = (
            "Extract 2-3 surprising or interesting nuggets from EACH document. "
            "Focus on things that would make someone say 'wait, really?'\n\n"
            f"{all_docs}"
        )
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["nuggets"] = exec_res
        print(f"  🔍 Extracted nuggets from {len(prep_res)} documents")


class WriteScript(Node):
    def prep(self, shared):
        """Read the extracted nuggets."""
        return shared["nuggets"]

    def exec(self, nuggets):
        """Generate a conversational podcast script between two hosts."""
        prompt = f"""Write a podcast script between two hosts: Alex and Jamie.

Source nuggets:
{nuggets}

Write ~6 exchanges (12 lines). Make it natural, with reactions and interruptions.
Output as YAML:
```yaml
script:
  - name: Alex
    line: "what Alex says"
  - name: Jamie
    line: "what Jamie says"
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)
        assert isinstance(result["script"], list)
        return result["script"]

    def post(self, shared, prep_res, exec_res):
        shared["script"] = exec_res
        print(f"  ✍️  Generated script with {len(exec_res)} lines")
        for item in exec_res:
            print(f"    {item['name']}: {item['line'][:80]}{'...' if len(item['line']) > 80 else ''}")


class TextToSpeech(Node):
    def prep(self, shared):
        """Read the podcast script."""
        return shared["script"]

    def exec(self, script):
        """Convert each line of the script to speech and concatenate."""
        audio_parts = []
        for i, item in enumerate(script):
            voice = VOICES.get(item["name"], "alloy")
            print(f"    🎙️  Generating audio for {item['name']} (line {i+1}/{len(script)})...")
            audio_data = text_to_speech(item["line"], voice=voice)
            audio_parts.append(audio_data)
        return b"".join(audio_parts)

    def post(self, shared, prep_res, exec_res):
        # Detect format: MP3 starts with ID3 or 0xff; otherwise raw PCM from Gemini
        is_mp3 = exec_res[:3] == b'ID3' or (len(exec_res) > 1 and exec_res[0] == 0xff)
        if is_mp3:
            out = shared.get("output_file", "podcast.mp3")
            with open(out, "wb") as f:
                f.write(exec_res)
        else:
            # Raw PCM from Gemini TTS — wrap in WAV (24kHz, 16-bit, mono)
            out = os.path.splitext(shared.get("output_file", "podcast.mp3"))[0] + ".wav"
            with wave.open(out, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(exec_res)
        shared["audio_file"] = out
        print(f"  ✅ Audio saved to {out}")
