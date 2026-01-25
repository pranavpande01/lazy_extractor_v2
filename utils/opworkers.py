import os,time,json
from agno.workflow.step import StepInput, StepOutput



def opworkers(step_input:StepInput):
    content = step_input.previous_step_content
    if hasattr(content, 'model_dump'):
        content = content.model_dump()
    
    workers_json=os.getenv("OPWORKERS_JSON")
    with open(workers_json,"w") as f:
        json.dump(content, f, indent=2)

    with open(workers_json,"r") as f:
        a = json.load(f)

    return StepOutput(content=json.dumps(a))
