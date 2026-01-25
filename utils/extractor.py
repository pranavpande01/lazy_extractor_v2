import os
import langextract as lx
from dotenv import load_dotenv

load_dotenv()

def extract(examples: list, text: str, prompt: str = "extract from the provided text. Make sure that the output formatting(dates, currencies,etc.) is processed as described in the examples and donot assume things by yourself."):
    a= lx.extract(
        text_or_documents=text,
        prompt_description=prompt,
        examples=examples,
            model_id="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    fence_output=True,
    use_schema_constraints=False,
    max_workers=3,
    extraction_passes=3


    )
    return a