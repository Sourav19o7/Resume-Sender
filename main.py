import os
import webbrowser
import subprocess
import time
import sys
from dotenv import load_dotenv

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = ["flask", "flask-cors", "langchain", "python-dotenv"]
    
    try:
        # Attempt to import key packages
        import flask
        import flask_cors
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "python-dotenv"])
        
    # Additional packages that might be needed
    try:
        import langchain
    except ImportError:
        print("Installing LangChain and related packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain", "langchain-openai", "langchain-anthropic"])

def create_sample_browser_use():
    """Create a sample browser_use.py file if it doesn't exist"""
    if not os.path.exists("browser_use.py"):
        print("Creating sample browser_use.py file...")
        with open("browser_use.py", "w") as f:
            f.write("""
class Agent:
    \"\"\"
    Sample Agent class that processes text using a language model.
    \"\"\"
    
    def __init__(self, task, llm):
        self.task = task
        self.llm = llm
    
    def run(self):
        \"\"\"Process the task and return a response\"\"\"
        from langchain.schema import HumanMessage
        
        messages = [HumanMessage(content=self.task)]
        response = self.llm.invoke(messages)
        return response.content
""")

def main():
    """
    Main entry point for the chatbot application.
    Starts the Flask server and opens the web interface.
    """
    # Load environment variables
    load_dotenv()
    
    print("\n🤖 Starting AI Chatbot...")
    
    # Check dependencies
    check_dependencies()
    
    # Make sure all necessary files exist
    required_files = ["index.html", "styles.css", "script.js", "server.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: {file} not found. Please make sure all files are in the current directory.")
            return
            
    # Check for browser_use.py or create a simple version
    if not os.path.exists("browser_use.py"):
        create_sample_browser_use()
    
    # Create the simple_agent.py as a fallback
    if not os.path.exists("simple_agent.py"):
        if os.path.exists("simple_agent.py"):
            print("Using existing simple_agent.py as fallback")
        else:
            print("Error: simple_agent.py not found.")
            return
    
    # Start the Flask server
    print("Starting server...")
    
    # Use a different approach based on OS
    if os.name == 'nt':  # Windows
        server_process = subprocess.Popen([sys.executable, "server.py"], 
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:  # Unix/Linux/Mac
        server_process = subprocess.Popen([sys.executable, "server.py"])
    
    # Give the server time to start
    time.sleep(2)
    
    # Open the web browser
    print("Opening browser...")
    webbrowser.open("http://localhost:5000")
    
    print("\n✅ Chatbot is now running!")
    print("- Access the interface at: http://localhost:5000")
    print("- Press Ctrl+C to quit\n")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down chatbot...")
        server_process.terminate()
        print("Goodbye!")

if __name__ == "__main__":
    main()