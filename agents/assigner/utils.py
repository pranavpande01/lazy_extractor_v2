import yaml

CONFIG_PATH="config.yaml"
with open(CONFIG_PATH) as f:
    CONFIG=yaml.safe_load(f)


AGENT_CONFIG=CONFIG["agent_config"]
INSTRUCTIONS=CONFIG["instructions"]
PROMPT=CONFIG["prompt_template_multi_workers"]


def get_prompt(worker_task:list,example_section:str)->None:
    return PROMPT.format(worker_task=worker_task,example_section=example_section)