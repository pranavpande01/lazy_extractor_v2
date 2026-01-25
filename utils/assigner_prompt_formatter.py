import json,time
from agno.workflow import StepInput,StepOutput
def assigner_prompt_formatter(step_input: StepInput):
    content = step_input.previous_step_content

    if isinstance(content, str):
        workers_data = json.loads(content)
    else:
        workers_data = content

    prompt = """You MUST assign rows to ALL of the following workers. Process each worker one by one and execute UPDATE statements for each.

DO NOT ask clarifying questions. DO NOT stop after one worker. Complete ALL workers before finishing.

Workers to assign:
"""

    for worker in workers_data.get("workers", []):
        prompt += f"{worker['name']} : {worker['purpose']}\n"
        prompt += f"\tExample Input:{worker['example_input_row']}\n"
        prompt += f"\tExample Output:{worker['example_output']}\n\n"

    prompt += """
IMPORTANT: You must execute UPDATE statements for ALL workers above. Do not stop until all workers have been assigned.
"""
    time.sleep(120)

    return StepOutput(content=prompt)
