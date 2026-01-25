import os,time
from agno.workflow.step import StepInput, StepOutput

def oprec(step_input:StepInput):
    oprec_md=os.getenv("OPREC_MD")
    with open(oprec_md,"w") as f:
        f.write(step_input.previous_step_content)

    with open(oprec_md,"r") as f:
        a=f.read()
    time.sleep(60)

    return StepOutput(content=f"{a}")
