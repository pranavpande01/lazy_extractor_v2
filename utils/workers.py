from pydantic import BaseModel, Field
from typing import Optional,List
class Worker(BaseModel):
    name: str = Field(description="Worker name")
    purpose: Optional[str] = Field(default=None, description="What the worker extracts")
    example_input_row: str = Field(
        description="The raw row text including sno"
    )
    example_output: str = Field(
        description="The JSON extraction result as a string"
    )

class WorkerList(BaseModel):
    workers: List[Worker] = Field(description="List of all workers proposed by the strategist")
