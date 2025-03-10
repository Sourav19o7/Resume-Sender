from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Try to import your Agent class
try:
    from browser_use import Agent
    print("Successfully imported Agent from browser_use.py")
except ImportError as e:
    print(f"Could not import Agent from browser_use.py: {e}")
    print("Using SimpleAgent as fallback")
    from simple_agent import SimpleAgent as Agent

# Load environment variables
load_dotenv()

# Configure Flask app
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)  # Enable CORS for all routes

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

@app.route('/', methods=['GET'])
def home():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "provider": LLM_PROVIDER})

@app.route('/chat', methods=['POST'])
def chat():
    """Handle incoming chat requests"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        try:
            # Initialize agent with user input
            agent = Agent(task=user_message, llm=llm)
            
            # Handle both synchronous and asynchronous run methods
            try:
                # First try the synchronous approach
                response = agent.run()
                return jsonify({"response": response})
            except Exception as e:
                if "coroutine" in str(e):
                    # If it's an async method, we need to run it differently
                    print("Detected async method, using asyncio to run it")
                    import asyncio
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(agent.run())
                    loop.close()
                    return jsonify({"response": response})
                else:
                    # Some other error occurred
                    raise e
                
        except Exception as inner_e:
            print(f"Error with agent: {inner_e}")
            # Fallback to direct model call if agent fails
            from langchain.schema import HumanMessage
            messages = [HumanMessage(content=user_message)]
            response = llm.invoke(messages).content
            return jsonify({"response": response})
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use 0.0.0.0 to make the server accessible from other machines
    print("\n🤖 Chatbot is running! Open http://localhost:5000 in your browser to use the chatbot interface.\n")
    app.run(host='0.0.0.0', port=5000, debug=True)