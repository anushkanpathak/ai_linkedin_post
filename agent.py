

class Agent:
    def __init__(self, name, role, goal, backstory, llm_fn):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm_fn = llm_fn

    def run(self, input_text):
        """
        Runs the LLM with combined input:
        - Goal + Backstory + Input
        """
        prompt = f"Agent Name: {self.name}\nRole: {self.role}\nGoal:\n{self.goal}\n"
        if self.backstory:
            prompt += f"Backstory:\n{self.backstory}\n"
        prompt += f"Input:\n{input_text}\n"

        try:
            response = self.llm_fn(prompt)
            return response
        except Exception as e:
            print(f"[{self.name} Error]: {e}")
            return f"Error: {self.name} failed to process input."
