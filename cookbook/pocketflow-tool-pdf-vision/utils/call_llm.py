import os
from openai import OpenAI
from pathlib import Path

# Get the project root directory (parent of utils directory)
ROOT_DIR = Path(__file__).parent.parent

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
