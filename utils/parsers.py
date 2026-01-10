from pydantic import BaseModel, Field
from typing import Optional, List
from agno.agent import Agent
from agno.models.google import Gemini

class Worker(BaseModel):
    name: str = Field(description="Worker name'")
    purpose: Optional[str] = Field(default=None, description="What the worker extracts")
    example_input_row: str = Field(
        description="The raw row text to extract from"
    )
    example_output: str = Field(
        description="The JSON extraction result as a string"
    )

class WorkerList(BaseModel):
    workers: List[Worker] = Field(description="List of all workers proposed by the strategist")


parse_worker=Agent(
    name="worker parser",
    instructions="""Parse the worker definitions from the previous agent into structured JSON.
    For each worker, extract:
    - name: the worker name (e.g. 'vendor_bill_header_worker')
    - purpose: what the worker extracts (optional, can be null)
    - example_input_row: the raw row text.
    - example_output: the JSON extraction result as a string
    
    Return a list of all workers.""",
    output_schema =WorkerList,
    model=Gemini(id="gemini-2.5-flash-lite",temperature=0)
)

extract_worker=Agent(
    name="worker extractor",
    instructions="""Simply provide the list of workers proposed by the previous agent. For every worker, I just want you to output the worker number, it's name, it's purpose, it's Example Input Row and Example Output
    Please be assure that this task is for a serious accounting workflow, and return the requested data WORD TO WORD as provided by the previous agent.
    DONOT MISQUOTE THE PREVIOUS AGENT AT ANY COST. DONOT INFER DEFINITIONS/CONTENT BY YOURSELF""",
    model=Gemini(id="gemini-2.5-flash-lite",temperature=0)
)
