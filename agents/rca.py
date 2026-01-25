import os, yaml
from pathlib import Path
from agno.agent import Agent
from dotenv import load_dotenv
from agno.models.google import Gemini
from agno.tools.file import FileTools
from agents.tools.tools import RCATools
load_dotenv()
db_path=os.getenv("DB_PATH")

CONFIG_PATH=Path("agents/config.yaml")
with open(CONFIG_PATH) as f:
    CONFIG=yaml.safe_load(f)

AGENT_CONFIG=CONFIG["rca_config"]
INSTRUCTIONS=CONFIG["rca_instructions"]


ZONE9_ROOT = Path("./")

tools=RCATools(db_path=db_path)

rca=Agent(
    name=AGENT_CONFIG["name"],
    model=Gemini(
        api_key=os.getenv("GOOGLE_API_KEY"),
        id=AGENT_CONFIG["model_id"],
        thinking_budget=AGENT_CONFIG.get("thinking_budget", 8192)
    ),
    tools=[
        tools.runsql,
        FileTools(base_dir=ZONE9_ROOT)  
    ],
    instructions=INSTRUCTIONS,
    markdown=True,
)
