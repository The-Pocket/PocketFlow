from pocketflow import Flow
from nodes import AnalyzeDocs, WriteScript, TextToSpeech


def create_podcast_flow():
    """
    Create a linear document-to-podcast flow.

    Pipeline:
    1. AnalyzeDocs   — extract interesting nuggets from source documents
    2. WriteScript   — generate a conversational podcast script
    3. TextToSpeech  — convert the script to audio using OpenAI TTS

    Returns:
        Flow: A complete podcast-generation flow
    """
    analyze = AnalyzeDocs()
    script = WriteScript()
    tts = TextToSpeech()

    # Linear chain
    analyze >> script >> tts

    return Flow(start=analyze)
