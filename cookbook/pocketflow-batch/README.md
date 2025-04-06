# Batch Translation Process

This project demonstrates a batch processing implementation that enables LLMs to translate documents into multiple languages simultaneously. It's designed to efficiently handle the translation of markdown files while preserving formatting.

## Features

- Translates markdown content into multiple languages in parallel
- Saves translated files to specified output directory

## Getting Started

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Set up your API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

3. Run the translation process:
```bash
python main.py
```

## How It Works

The implementation uses a `TranslateTextNode` that processes batches of translation requests:

```mermaid
flowchart LR
    batch[TranslateTextNode]
```

The `TranslateTextNode`:
1. Prepares batches for multiple language translations
2. Executes translations in parallel using the model
3. Saves the translated content to individual files
4. Maintains the original markdown structure

This approach demonstrates how PocketFlow can efficiently process multiple related tasks in parallel.

## Example Output

When you run the translation process, you'll see output similar to this:

```
Translated Chinese text
Translated Spanish text
Translated Japanese text
Translated German text
Translated Russian text
Translated Portuguese text
Translated French text
Translated Korean text
Saved translation to translations/README_CHINESE.md
Saved translation to translations/README_SPANISH.md
Saved translation to translations/README_JAPANESE.md
Saved translation to translations/README_GERMAN.md
Saved translation to translations/README_RUSSIAN.md
Saved translation to translations/README_PORTUGUESE.md
Saved translation to translations/README_FRENCH.md
Saved translation to translations/README_KOREAN.md

=== Translation Complete ===
Translations saved to: translations
============================
```

## Files

- [`main.py`](./main.py): Implementation of the batch translation node
- [`utils.py`](./utils.py): Simple wrapper for calling the Anthropic model
- [`requirements.txt`](./requirements.txt): Project dependencies

The translations are saved to the `translations` directory, with each file named according to the target language.