"""
Simple Agent module that can be used if the original browser_use.Agent is causing issues.
This provides a simplified fallback implementation.
"""

class SimpleAgent:
    """A simple agent that can process text prompts."""
    
    def __init__(self, task, llm):
        """
        Initialize the SimpleAgent.
        
        Args:
            task (str): The input message or task
            llm: The language model to use for responses
        """
        self.task = task
        self.llm = llm
        
    def run(self):
        """
        Process the task and return a response.
        
        Returns:
            str: The response to the task
        """
        try:
            # Try to use the provided LLM
            from langchain.schema import HumanMessage
            
            messages = [HumanMessage(content=self.task)]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error using LLM: {e}")
            
            # Fallback to a simple response if LLM fails
            return f"I received your message about '{self.task[:50]}...' but I'm having trouble generating a detailed response right now. Please try again with a different question."