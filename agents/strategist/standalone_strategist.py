import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))  # adds the script's own directory
from tools import StrategistTools
from prompts import AGENT_CONFIG, INSTRUCTIONS, get_prompt

import os
from agno.agent import Agent
from agno.tools.sql import SQLTools
from agno.tools import Toolkit
from agno.models.google import Gemini
from dotenv import load_dotenv
load_dotenv()

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
