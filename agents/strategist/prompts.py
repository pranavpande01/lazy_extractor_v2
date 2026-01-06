import yaml

CONFIG_PATH="config.yaml"
with open(CONFIG_PATH) as f:
    CONFIG=yaml.safe_load(f)


AGENT_CONFIG=CONFIG["agent_config"]
INSTRUCTIONS=CONFIG["instructions"]
PROMPT=CONFIG["prompt"]


def get_prompt(field_spec:list,examples:str,db_path:str,ocr_folder:str)->None:
    pass