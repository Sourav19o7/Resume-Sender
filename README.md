# AI Chatbot Interface

A minimalistic dark mode AI chatbot interface that connects to your LLM of choice using LangChain.

## Features

- 🌙 **Dark Mode UI**: Modern, clean dark theme with light mode toggle
- 🤖 **LLM Integration**: Works with both Anthropic and OpenAI models
- 💬 **Interactive Chat**: Fully interactive chatbot experience
- 🧩 **Code Syntax**: Support for code blocks with syntax highlighting
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Setup

1. Install the required dependencies:

```bash
pip install flask flask-cors langchain-openai langchain-anthropic python-dotenv
```

2. Set up your `.env` file with API keys:

```
# Choose your LLM provider: "openai" or "anthropic"
LLM_PROVIDER=anthropic

# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

3. Make sure you have the `browser_use.py` file with your `Agent` class.

## Running the Chatbot

Simply run:

```bash
python main.py
```

This will:
1. Start the Flask server
2. Open your web browser to the chatbot interface
3. Allow you to interact with your AI model through the UI

You can also run the server directly:

```bash
python server.py
```

Then open `http://localhost:5000` in your browser.

## Files Overview

- `main.py`: Entry point script that launches the application
- `server.py`: Flask server that connects to your LangChain Agent
- `index.html`: Main chatbot UI
- `styles.css`: Custom styling and animations
- `script.js`: UI interaction and chat functionality
- `tailwind.config.js`: Tailwind CSS configuration

## Customization

You can easily customize the UI by modifying the Tailwind classes in `index.html` or updating the color scheme in `tailwind.config.js`.

## License

MIT