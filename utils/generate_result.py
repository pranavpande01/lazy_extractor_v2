import pandas as pd
import os,sqlite3,json
from functools import partial
from dotenv import load_dotenv
from utils.extractor import extract
from utils.adapter_factory import generate_adapter
from agno.workflow.step import StepInput, StepOutput

load_dotenv()

def generate_result(step_input: StepInput):

    db_path = os.getenv("DB_PATH")
    conn = sqlite3.connect(db_path)
    cols = 'sno, text, page_no, worker'
    df = pd.read_sql_query(f'SELECT {cols} FROM rows ORDER BY sno', conn)
    conn.close()
    workers_json=os.getenv("OPWORKERS_JSON")
    with open(workers_json,"r") as f:
        a=json.load(f)

    func_map = {i["name"]:partial(extract,examples=generate_adapter(i)) for i in a["workers"]}

    def safe_extract(row):
        if pd.isna(row["worker"]) or row["worker"] not in func_map:
            return None
        try:
            extractions = func_map[row["worker"]](text=row["text"]).extractions
            result = {}
            for i in extractions:
                if i.extraction_class in i.attributes:
                    result[i.extraction_class] = i.attributes[i.extraction_class]
                elif i.attributes:
                    result[i.extraction_class] = i.attributes
                else:
                    result[i.extraction_class] = i.extraction_text
            return StepOutput(content=str(result))
        except Exception as e:
            print(f"Error extracting row {row['sno']}: {e}")
            return StepOutput(content=e)

    df["result"] = df.apply(safe_extract, axis=1)

    conn = sqlite3.connect(db_path)

    extractions_df = df[["sno","text","worker", "result"]].copy()
    extractions_df["result"] = extractions_df["result"].apply(lambda x: json.dumps(x) if x else None)
    extractions_df.to_sql("extractions", conn, if_exists="replace", index=False)

    conn.close()
    return StepOutput(content="EXTRACTION SUCCESSFULLY DONE")
