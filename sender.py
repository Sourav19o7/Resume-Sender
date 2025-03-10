import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from browser_use import Agent

# Load environment variables
load_dotenv()

# Check which LLM provider to use (default: Anthropic)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").lower()

# Set API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Validate API key availability
if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY. Please set it in your .env file.")
elif LLM_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
    raise ValueError("Missing ANTHROPIC_API_KEY. Please set it in your .env file.")

# Select the appropriate LLM
if LLM_PROVIDER == "openai":
    llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
elif LLM_PROVIDER == "anthropic":
    llm = ChatAnthropic(model="claude-3-haiku-20240307", api_key=ANTHROPIC_API_KEY)
else:
    raise ValueError("Invalid LLM_PROVIDER. Use 'openai' or 'anthropic'.")

async def chat():
    """Interactive chatbot loop"""
    print("\n🤖 Chatbot is running! Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        # Initialize agent with user input
        agent = Agent(task=user_input, llm=llm)

        try:
            response = await agent.run()
            print(f"Bot: {response}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    asyncio.run(chat())
