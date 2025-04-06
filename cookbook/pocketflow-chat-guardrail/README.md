#  Travel Advisor Chat with Guardrails

A travel-focused chat application using PocketFlow with OpenAI's GPT-4o model, enhanced with input validation to ensure only travel-related queries are processed.

## Features

- Travel advisor chatbot that answers questions about destinations, planning, accommodations, etc.
- **Topic-specific guardrails** to ensure only travel-related queries are accepted

## Run It

1. Make sure your OpenAI API key is set:
    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```
    Alternatively, you can edit the `utils.py` file to include your API key directly.

2. Install requirements and run the application:
    ```bash
    pip install -r requirements.txt
    python main.py
    ```

## How It Works

```mermaid
flowchart LR
    user[UserInputNode] -->|validate| guardrail[GuardrailNode]
    guardrail -->|retry| user
    guardrail -->|process| llm[LLMNode]
    llm -->|continue| user
```

The chat application uses:
- A `UserInputNode` that collects user input in its `exec` method
- A `GuardrailNode` that validates if the query is travel-related using:
  - Basic validation checks (empty input, too short)
  - LLM-based validation to determine if the query relates to travel
- An `LLMNode` that processes valid travel queries using GPT-4o with a travel advisor system prompt
- Flow connections that route inputs through validation before processing and handle retries for non-travel related queries

## Files

- [`main.py`](./main.py): Implementation of the nodes and chat flow
- [`utils.py`](./utils.py): Utilities for calling the OpenAI API

## Example Outputs

``` 
Welcome to the Travel Advisor Chat! Type 'exit' to end the conversation.

You: Plan my trip to Thailand

Travel Advisor: Thailand offers a blend of vibrant cities, serene beaches, and rich culture. Begin in Bangkok to explore the Grand Palace and local markets. Head north to Chiang Mai for temples and elephant sanctuaries. Fly south to the islands; Phuket or Koh Samui for beaches, diving, and nightlife. Consider visiting during the cool season (November-February) for pleasant weather. Accommodation ranges from budget hostels to luxury resorts. Internal flights, trains, and buses connect major destinations. Don’t miss local cuisine, from street food to fine dining. Ensure your passport is valid for six months and consider travel insurance for peace of mind. Enjoy!

You: exit

Goodbye! Safe travels!
```

```
Welcome to the Travel Advisor Chat! Type 'exit' to end the conversation.

You: How to study large language models?

Travel Advisor: The query is not related to travel advice, destinations, planning, or other travel topics. It is about studying large language models, which is a topic related to artificial intelligence and machine learning.

You: exit

Goodbye! Safe travels!
```