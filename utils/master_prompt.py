import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.yaml"
with open(CONFIG_PATH) as f:
    CONFIG=yaml.safe_load(f)


PROMPT=CONFIG["master_prompt"]


def get_prompt(fields_fmt:list,examples:str,db_path:str,ocr_folder:str,other_instructions=None)->str:
    if other_instructions:
        return PROMPT.format(fields_fmt=fields_fmt,examples=examples,db_path=db_path,ocr_folder=ocr_folder,other_instructions=other_instructions)
    return PROMPT.format(fields_fmt=fields_fmt,examples=examples,db_path=db_path,ocr_folder=ocr_folder,other_instructions="None")