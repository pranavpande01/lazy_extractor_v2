from agno.agent import Agent
from utils.workers import WorkerList
from agno.models.google import Gemini

extract_workers=Agent(
    name="worker extractor",
    instructions="""Simply provide the list of workers proposed by the previous agent. For every worker, I just want you
    to output the worker number, it's name, it's purpose, it's Example Input Row and Example Output
    Please be assure that this task is for a serious accounting workflow, and return the requested data WORD TO WORD as provided by the previous agent.
    DONOT INCLUDE ANY ASSIGNMENT RULES PROPOSED BY THE PREVIOUS AGENT.
    DONOT MISQUOTE THE PREVIOUS AGENT AT ANY COST. DONOT INFER DEFINITIONS/CONTENT BY YOURSELF""",
    model=Gemini(id="gemini-2.5-flash-lite",temperature=0)
)

extract_validators=Agent(
    name="validator extractor",
        instructions="""Simply provide the list of validation strategies proposed by the previous agent. For every worker, I just want you
    to output the associated validation strategy proposed by the previous agent.
    Please be assure that this task is for a serious accounting workflow, and return the requested data WORD TO WORD as provided by the previous agent
        DONOT MISQUOTE THE PREVIOUS AGENT AT ANY COST. DONOT INFER DEFINITIONS/CONTENT BY YOURSELF""",

    model=Gemini(id="gemini-2.5-flash-lite",temperature=0)
)

extract_reconstructions=Agent(
    name="reconstruction extractor",
        instructions="""Simply provide the reconstruction logic proposed by the previous agent.
    Extract ONLY the "Reconstruction Logic" section that explains how worker outputs are combined into the final JSON.
    Return the reconstruction steps WORD TO WORD as provided by the previous agent.
    Please be assured that this task is for a serious accounting workflow.
    DONOT MISQUOTE THE PREVIOUS AGENT AT ANY COST. DONOT INFER DEFINITIONS/CONTENT BY YOURSELF""",

    model=Gemini(id="gemini-2.5-flash-lite",temperature=0)
)

parse_workers=Agent(
    name="worker parser",
        instructions="""Parse the worker definitions from the previous agent into structured JSON.
    For each worker, extract:
    - name: the worker name (e.g. 'vendor_bill_header_worker')
    - purpose: what the worker extracts (optional, can be null)
    - example_input_row: the raw row text (e.g. "Bennett, Coleman And Co. Ltd., Vide Bill: BCKA25RV-0017632 Dated: 26 09 2025")
    - example_output: the JSON extraction result as a string
    
    Return a list of all workers.""",
    output_schema =WorkerList,
    model=Gemini(id="gemini-2.5-flash",temperature=0)
)