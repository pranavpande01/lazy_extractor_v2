import langextract as lx
import json
def generate_adapter(b:dict):
    examples = [
        lx.data.ExampleData(
            text=b["example_input_row"],
            extractions=[
                lx.data.Extraction(
                    extraction_class=i,
                    extraction_text=str(j),
                    attributes={i:j}
                )
                for i,j in json.loads(b['example_output']).items()]
        )
    ]

    return examples
