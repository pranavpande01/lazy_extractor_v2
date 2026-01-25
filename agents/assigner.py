import os,yaml
from pathlib import Path
from agno.agent import Agent
from agno.tools import Toolkit
from dotenv import load_dotenv
from agno.models.google import Gemini
from agents.tools.tools import AssignerTools
load_dotenv()
db_path=os.getenv("DB_PATH")
ocr_folder=os.getenv("OCR_FOLDER")

CONFIG_PATH=Path("agents/config.yaml")
with open(CONFIG_PATH) as f:
    CONFIG=yaml.safe_load(f)

AGENT_CONFIG=CONFIG["assigner_config"]
INSTRUCTIONS=CONFIG["assigner_instructions"]


tools=AssignerTools(db_path=db_path, ocr_folder=ocr_folder)
tools_funcs = [tools.view_page, tools.runsql]
toolkit = Toolkit(name="AssignerTools", tools=tools_funcs)
assigner=Agent(
    name="assigner",
    model=Gemini(
        id=AGENT_CONFIG["model_id"],
        thinking_budget=AGENT_CONFIG["thinking_budget"],
        include_thoughts=True
    ),
    tools=[toolkit],
    instructions=INSTRUCTIONS,
    reasoning_max_steps=AGENT_CONFIG["reasoning_max_steps"],
    reasoning_min_steps=AGENT_CONFIG["reasoning_min_steps"]
)