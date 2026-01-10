from agno.workflow import Workflow
from agents.assigner.standalone_assigner import assigner
from agents.strategist.standalone_strategist import strategist

from agno.workflow import Parallel, Steps, Workflow, Steps
from utils.printers import printer1,printer2,printer3,printer4,printer5,printer6, reset_db_worker_column, generate_result, assigner_prompt_formatter
from utils.extractor import extract as extractor 
from utils.parsers import parse_worker,extract_worker
from data.prompt_builder import EXAMPLES, FIELD_SPEC
from agents.strategist.prompts import get_prompt

import os
from dotenv import load_dotenv
load_dotenv("/workspaces/lazy_extractor_v2/.env")

db_path=os.getenv("DB_PATH")
ocr_folder=os.getenv("OCR_FOLDER")

strategist_workflow = Workflow(
    name="Main Workflow",
    steps=[
        strategist,
        printer1,
        Parallel(
            Steps(name="worker extractor chain",steps=[extract_worker,printer2,parse_worker,printer5,reset_db_worker_column,assigner_prompt_formatter,assigner,printer6,generate_result])
        )
    ]
)

STRATEGIST_PROMPT = get_prompt(
    fields_fmt=FIELD_SPEC,
    examples=EXAMPLES,
    db_path=db_path,
    ocr_folder=ocr_folder
)




strategist_workflow.print_response(STRATEGIST_PROMPT,stream=True,stream_events=True)
