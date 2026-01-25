import os,yaml
from pathlib import Path
from agno.agent import Agent
from agno.tools import Toolkit
from dotenv import load_dotenv
from agno.tools.sql import SQLTools
from agno.models.google import Gemini
from agents.tools.tools import StrategistTools

load_dotenv()

CONFIG_PATH=Path("agents/config.yaml")
with open(CONFIG_PATH) as f:
    CONFIG=yaml.safe_load(f)

AGENT_CONFIG=CONFIG["strategist_config"]
INSTRUCTIONS=CONFIG["strategist_instructions"]

db_path=os.getenv("DB_PATH")
ocr_folder=os.getenv("OCR_FOLDER")

tools=StrategistTools(db_path,ocr_folder)
toolkit=Toolkit(name="strategist_tools",tools=[tools.view_page])

strategist_tools=[SQLTools(db_url=f"sqlite:///{db_path}"), toolkit]

strategist=Agent(
    name="strategist",
    model=Gemini(
        id=AGENT_CONFIG["model_id"],
        thinking_budget=AGENT_CONFIG["thinking_budget"],
        include_thoughts=True

    ),
    tools=strategist_tools,
    instructions=INSTRUCTIONS,
    markdown=True
)