import yaml

CONFIG_PATH="config.yaml"
with open(CONFIG_PATH) as f:
    CONFIG=yaml.safe_load(f)


AGENT_CONFIG=CONFIG["agent_config"]
INSTRUCTIONS=CONFIG["instructions"]
PROMPT=CONFIG["prompt_template"]


def get_prompt(fields_fmt:list,examples:str,db_path:str,ocr_folder:str)->None:
    return PROMPT.format(fields_fmt=fields_fmt,examples=examples,db_path=db_path,ocr_folder=ocr_folder)