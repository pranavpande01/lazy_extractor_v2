import os,time
from agno.workflow.step import StepInput, StepOutput

def oprca(step_input:StepInput):
    rca_md=os.getenv("OPRCA_MD")
    with open(rca_md,"w") as f:
        f.write(step_input.previous_step_content)

    with open(rca_md,"r") as f:
        a=f.read()
    time.sleep(20)

    return StepOutput(content=f"{a}")
