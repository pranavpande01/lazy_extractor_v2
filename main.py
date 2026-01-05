from agno.workflow import Workflow
from agents.assigner.standalone_assigner import agent as assigner
from agno.workflow import Parallel, Steps, Workflow, Steps
from agents.strategist.standalone_strategist import agent as strategist
from utils.printers import printer1,printer2,printer3,printer4,printer5,printer6
from utils.processing import extractor,parser

from utils.processing import parser,extract_reconstruction,extractor,extract_validator
from utils.db_ops import reset_db_worker_column,generate_result
from utils.agent_ops import assigner_prompt_formatter

strategist_workflow = Workflow(
    name="Strategist Workflow",
    steps=[
        strategist,
        printer1,
        Parallel(
            Steps(name="worker extractor chain",steps=[extractor,printer2,parser,printer5,reset_db_worker_column,assigner_prompt_formatter,assigner,printer6,generate_result]),
            Steps(name="validator extractor chain",steps=[extract_validator,printer3]),
            Steps(name="reconstruction extractor chain",steps=[extract_reconstruction,printer4])
        )
    ]
)


