import os, yaml
from pathlib import Path
from agno.agent import Agent
from dotenv import load_dotenv
from agno.tools import Toolkit
from agno.models.google import Gemini
from agno.tools.file import FileTools
from agents.tools.tools import ReconstructorTools
load_dotenv()
db_path=os.getenv("DB_PATH")
ocr_folder=os.getenv("OCR_FOLDER")

CONFIG_PATH=Path("agents/config.yaml")
with open(CONFIG_PATH) as f:
    CONFIG=yaml.safe_load(f)

AGENT_CONFIG=CONFIG["reconstructor_config"]
INSTRUCTIONS=CONFIG["reconstructor_instructions"]


tools=ReconstructorTools(db_path=db_path)

reconstructor=Agent(
    name=AGENT_CONFIG["name"],
    model=Gemini(
        api_key=os.getenv("GOOGLE_API_KEY"),
        id=AGENT_CONFIG["model_id"],
        thinking_budget=AGENT_CONFIG.get("thinking_budget", 4096)
    ),
    tools=[
        tools.runsql,
        FileTools(base_dir=Path("../data/tmp"))
    ],
    instructions=INSTRUCTIONS,
    markdown=True,
)