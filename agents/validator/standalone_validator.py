from pathlib import Path
from agno.agent import Agent
from agno.tools.file import FileTools
from dotenv import load_dotenv
from agno.models.google import Gemini
import yaml
import os

load_dotenv("/workspaces/lazy_extractor_v2/.env")

CONFIG_PATH = Path(__file__).parent / "config.yaml"
with open(CONFIG_PATH) as f:
    CONFIG = yaml.safe_load(f)

AGENT_CONFIG = CONFIG["agent_config"]
INSTRUCTIONS = CONFIG["instructions"]
PROMPT_TEMPLATE = CONFIG.get("prompt_template", "")

markdown_dir = Path("/workspaces/lazy_extractor_v2/data")

validator = Agent(
    name=AGENT_CONFIG["name"],
    model=Gemini(
        api_key=os.getenv("GOOGLE_API_KEY"),
        id=AGENT_CONFIG["model_id"],
        thinking_budget=AGENT_CONFIG.get("thinking_budget", 4096)
    ),
    tools=[FileTools(base_dir=markdown_dir)],
    instructions=INSTRUCTIONS,
    markdown=True,
)
 