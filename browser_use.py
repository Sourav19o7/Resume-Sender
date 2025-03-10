
class Agent:
    """
    Sample Agent class that processes text using a language model.
    """
    
    def __init__(self, task, llm):
        self.task = task
        self.llm = llm
    
    def run(self):
        """Process the task and return a response"""
        from langchain.schema import HumanMessage
        
        messages = [HumanMessage(content=self.task)]
        response = self.llm.invoke(messages)
        return response.content
