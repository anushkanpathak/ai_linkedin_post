
import os
from agent import Agent
from my_llm import call_llm  

AGENT_FOLDER = "agents"

def load_agent_from_file(name, role, filename):
    """Load goal/backstory from a text file and create an Agent instance"""
    path = os.path.join(AGENT_FOLDER, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} not found in agents folder.")
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    goal, backstory = "", ""
    if "Goal:" in content:
        parts = content.split("Goal:")[1]
        if "Backstory:" in parts:
            goal_part, backstory_part = parts.split("Backstory:")
            goal = goal_part.strip()
            backstory = backstory_part.strip()
        else:
            goal = parts.strip()
    else:
        goal = content.strip()

    return Agent(name=name, role=role, goal=goal, backstory=backstory, llm_fn=call_llm)

def run_crew(transcript):
    reader = load_agent_from_file("TranscriptReader", "Analyzer", "reader.txt")
    writer = load_agent_from_file("PostWriter", "LinkedInWriter", "writer.txt")
    reviewer = load_agent_from_file("Reviewer", "Editor", "reviewer.txt")
    story = reader.run(transcript)
    post = writer.run(story)
    final_post = reviewer.run(post)
    return final_post
