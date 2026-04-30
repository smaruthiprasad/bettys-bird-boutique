import os
from google.adk.agents import Agent
from google.adk.tools import google_search, AgentTool

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "search-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

model = "gemini-2.5-flash"

search_agent = Agent(
    name="search_agent",
    description="An agent that searches the web for general information about birds.",
    instruction=instruction,
    model=model,
    tools=[google_search],
)

search_agent_tool = AgentTool(agent=search_agent)
