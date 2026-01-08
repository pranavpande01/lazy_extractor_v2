import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))  
from tools import StrategistTools
from prompts import AGENT_CONFIG, INSTRUCTIONS, get_prompt
from assets import EXAMPLES
import os
from agno.agent import Agent
from agno.tools.sql import SQLTools
from agno.tools import Toolkit
from agno.models.google import Gemini
from dotenv import load_dotenv
load_dotenv("/workspaces/lazy_extractor_v2/.env")

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

prompt = get_prompt(
        fields_fmt=["vendor_bill_number","vendor_name","vendor_bill_date","total_vendor_gross","publications:{publication_name,city,ad_date,pdf_page_number,ad_size}"],
        examples=EXAMPLES,
        db_path=db_path,
        ocr_folder=ocr_folder
)

strategist.print_response(prompt, stream=True, stream_events=True)

