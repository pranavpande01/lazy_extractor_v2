import langextract as lx

def extract(examples: list, text: str, prompt: str = "extract from the provided text"):
    a= lx.extract(
        text_or_documents=text,
        prompt_description=prompt,
        examples=examples,
            model_id="gpt-4o",
    api_key="",
    fence_output=True,
    use_schema_constraints=False,
    max_workers=3,
    extraction_passes=3


    )
    return a