
class Task:
    def __init__(self, name, agent, description):
        self.name = name
        self.agent = agent
        self.description = description
        self.output = None

    def run(self, context_str):
       
        prompt = f"{self.description}\n\nPrevious context:\n{context_str}"
        result = self.agent.run(prompt)
        self.output = result
        return result
