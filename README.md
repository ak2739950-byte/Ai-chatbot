# AI Chatbot with NLP

An intelligent AI-based chatbot that understands user queries and responds intelligently using Natural Language Processing.

## Features

- **Intent Recognition**: Identifies user intent from natural language input
- **Pattern Matching**: Uses word similarity algorithms for flexible matching
- **Conversation Management**: Tracks conversation history and context
- **Extensible Design**: Easy to add new intents and responses
- **Session Statistics**: Provides conversation analytics

## Requirements

- Python 3.7+

No external dependencies required - uses only standard library modules.

## Installation

1. Clone or download this project
2. Navigate to the chatbot directory

```bash
cd chatbot
```

## Usage

Run the chatbot:

```bash
python main.py
```

### Interactive Commands

- Type your message and press Enter to chat
- Type `quit`, `exit`, or `bye` to end the conversation

## Project Structure

```
chatbot/
├── main.py        # Main chatbot implementation
├── intents.json   # Intent definitions and responses
├── requirements.txt
└── README.md
```

## How It Works

1. **Input Preprocessing**: User input is cleaned and normalized
2. **Tokenization**: Text is split into individual words
3. **Intent Recognition**: Compares input against known patterns using similarity scoring
4. **Response Generation**: Returns appropriate response based on recognized intent
5. **Conversation Tracking**: Stores history for analytics

## Customization

Edit `intents.json` to add new intents:

```json
{
  "tag": "new_intent",
  "patterns": ["pattern1", "pattern2"],
  "responses": ["Response 1", "Response 2"]
}
```

## License

MIT License