import os,time
from agno.workflow.step import StepInput, StepOutput

def oprecs(step_input:StepInput):
    reconstruction_md=os.getenv("OPRECS_MD")
    with open(reconstruction_md,"w") as f:
        f.write(step_input.previous_step_content)

    with open(reconstruction_md,"r") as f:
        a=f.read()
    time.sleep(20)

    return StepOutput(content=f"{a}")
