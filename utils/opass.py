import os,time
from agno.workflow.step import StepInput, StepOutput

def opass(step_input:StepInput):
    opass_md=os.getenv("OPASS_MD")
    with open(opass_md,"w") as f:
        f.write(step_input.previous_step_content)

    with open(opass_md,"r") as f:
        a=f.read()
    time.sleep(20)

    return StepOutput(content=f"{a}")
