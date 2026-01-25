
import os,time,json,sqlite3
from dotenv import load_dotenv
from agno.workflow.step import StepInput, StepOutput

load_dotenv()
db_path=os.getenv("DB_PATH")
def reset_db_worker_column(step_input: StepInput):
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE rows SET worker = NULL")
    conn.commit()
    conn.close()
    time.sleep(20)

    return StepOutput(content=step_input.previous_step_content)
