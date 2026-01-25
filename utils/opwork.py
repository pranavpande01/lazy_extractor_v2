import os,time
from agno.workflow.step import StepInput, StepOutput


def opwork(step_input:StepInput):
    opstrat_md=os.getenv("OPWORK_MD")
    with open(opstrat_md,"w") as f:
        f.write(str(step_input.previous_step_content))
    
    with open(opstrat_md,"r") as f:
        a=f.read()
    time.sleep(20)
    return StepOutput(content=f"{a}")

