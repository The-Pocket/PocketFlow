# PocketFlow Communication Example

This example demonstrates the [Communication](https://the-pocket.github.io/PocketFlow/communication.html) concept in PocketFlow, specifically focusing on the Shared Store pattern.

## Overview

The example implements a simple word counter that shows how nodes can communicate using a shared store. It demonstrates:

- How to initialize and structure a shared store
- How nodes can read from and write to the shared store
- How to maintain state across multiple node executions
- Best practices for shared store usage

## Project Structure

```
pocketflow-communication/
├── README.md
├── requirements.txt
├── main.py
├── flow.py
└── nodes.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Enter text when prompted. The program will:
1. Count words in the text
2. Store statistics in the shared store
3. Display running statistics (total texts, total words, average)

Enter 'q' to quit.

## How it Works

The example uses three nodes:

1. `TextInput`: Reads user input and initializes the shared store
2. `WordCounter`: Counts words and updates statistics in the shared store
3. `ShowStats`: Displays statistics from the shared store

This demonstrates how nodes can share and maintain state using the shared store pattern. 