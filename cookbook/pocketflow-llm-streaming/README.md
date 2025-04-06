#  LLM Streaming and Interruption

Demonstrates real-time LLM response streaming with user interrupt capability.

## Features

- Real-time display of LLM responses as they're generated
- User interrupt with ENTER key at any time

## Run It

```bash
pip install -r requirements.txt
python main.py
```

## How It Works

StreamNode:
1. Creates interrupt listener thread
2. Fetches content chunks from LLM
3. Displays chunks in real-time
4. Handles user interruption

## API Key

By default, demo uses fake streaming responses. To use real OpenAI streaming:

1. Edit main.py to replace the fake_stream_llm with stream_llm:
```python
# Change this line:
chunks = fake_stream_llm(prompt)
# To this:
chunks = stream_llm(prompt)
```

2. Make sure your OpenAI API key is set:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Files

- `main.py`: StreamNode implementation
- `utils.py`: Real and fake LLM streaming functions
 