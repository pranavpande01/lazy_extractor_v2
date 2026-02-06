# Lazy Extractor V2

An AI-powered multi-agent system for extracting structured data from documents using advanced OCR and large language models.

## Overview

Lazy Extractor V2 automates entity extraction from complex documents (invoices, bills, forms, reports, etc.) by leveraging a sophisticated 8-stage pipeline where AI agents collaborate to understand document structure, design extraction strategies, and produce high-quality structured JSON output.

**Key Innovation**: No hand-coded extraction rules. AI agents intelligently design extraction workers based on document analysis.

## Architecture

The system employs a collaborative multi-agent pipeline:

```
Document Image
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. OCR (PaddleOCR)                                          │
│    Extract text fragments with bounding box coordinates     │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Row Builder                                              │
│    Merge OCR fragments into logical rows based on position  │
│    Store in SQLite with layout metadata                     │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Strategist Agent 🧠                                     │
│    Design extraction workers and validation strategies      │
│    Use SQL + page images to understand document structure   │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Assigner Agent 🎯                                       │
│    Map rows to workers using pattern matching              │
│    Generate SQL UPDATE statements for assignments           │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Worker Extraction 🔧                                    │
│    Extract fields using LangExtract (one row = one entity)  │
│    Store results in extractions table                       │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Validator Agent ✅                                      │
│    Validate extraction results against rules               │
│    Perform root cause analysis on failures                 │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Reconstructor Agent 🏗️                                 │
│    Combine worker outputs into final nested JSON           │
│    Apply grouping and carry-forward logic via SQL          │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. RCA Agent 🔍                                             │
│    Root cause analysis of pipeline failures                │
│    Review agent outputs and identify issues                │
└─────────────────────────────────────────────────────────────┘
    ↓
Final JSON Output
```

## Agent Roles

### 1. Strategist Agent
- **Analyzes** expected output examples and field structure
- **Explores** document rows via SQL queries and page images
- **Designs** extraction workers with:
  - Purpose and assignment rules
  - Example input/output pairs
  - Validation strategies
- **Recommends** reconstruction logic or row restructuring if needed

### 2. Assigner Agent
- **Routes** database rows to appropriate workers
- **Uses** anchor-based pattern matching for robustness
- **Supports** multi-page documents with repeating structures
- **Generates** SQL UPDATE statements to assign rows

### 3. Worker Layer
- **Extracts** fields from individual rows
- **Uses** LangExtract library for structured extraction
- **Based on** worker definitions provided by Strategist
- **Constraint**: One row must contain exactly one entity

### 4. Validator Agent
- **Checks** extraction results for correctness
- **Validates** against rules defined by Strategist
- **Performs** root cause analysis on failures
- **Identifies** assignment or schema mismatches

### 5. Reconstructor Agent
- **Combines** worker outputs into final JSON
- **Groups** data based on reconstruction logic
- **Handles** cross-worker relationships (e.g., page numbers applied to items)
- **Uses** SQL with CTEs and JSON functions for efficient grouping

### 6. RCA Agent
- **Analyzes** pipeline failures
- **Reviews** agent outputs and context
- **Identifies** where agents messed up
- **Suggests** improvements to strategy or assignments

## Installation

### Requirements
- Python 3.8+
- SQLite3
- API Keys: Google Gemini, OpenAI

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/pranavpande01/lazy_extractor_v2.git
cd lazy_extractor_v2
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (`.env`):
```env
# API Keys
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key

# Paths
DB_PATH=/path/to/your/database.db
OCR_FOLDER=/path/to/ocr/images

# Output files
OPSTRAT_MD=/path/to/output/strategy.md
OPWORK_MD=/path/to/output/workers.md
OPASS_MD=/path/to/output/assignments.md
OPREC_MD=/path/to/output/reconstruction.md
OPRECS_MD=/path/to/output/reconstructions.md
OPWORKERS_JSON=/path/to/output/workers.json
OPVALS_MD=/path/to/output/validators.md
OPRCA_MD=/path/to/output/rca.md
OPASSPRO_MD=/path/to/output/assigner_pro.md
```

## Usage

### Basic Workflow

```python
from agents.strategist import strategist
from agents.assigner import assigner
from agents.reconstructor import reconstructor
from utils.generate_result import generate_result

# Define what to extract
field_structure = {
    "vendor": {"name", "address", "email"},
    "items": [{"description", "quantity", "price"}],
    "total": {"amount", "tax"}
}

examples = """
{
  "vendor": {
    "name": "ACME Corp",
    "address": "123 Main St",
    "email": "info@acme.com"
  },
  "items": [
    {"description": "Widget", "quantity": 10, "price": 5.00}
  ],
  "total": {"amount": 50.00, "tax": 5.00}
}
"""

# 1. Strategist designs extraction workers
strategist_response = strategist.run(f"""
Design extraction workers for this document structure:
{field_structure}

Example output:
{examples}
""")

# 2. Assigner maps rows to workers
assigner_response = assigner.run(f"""
Assign rows to workers based on this strategy:
{strategist_response}
""")

# 3. Reconstructor combines results
reconstructor_response = reconstructor.run("""
Reconstruct the final JSON from extractions
""")
```

## Project Structure

```
lazy_extractor_v2/
├── agents/
│   ├── strategist.py          # Worker strategy designer
│   ├── assigner.py            # Row-to-worker mapper
│   ├── reconstructor.py       # Final JSON builder
│   ├── rca.py                 # Root cause analyzer
│   ├── config.yaml            # Agent configurations & instructions
│   └── tools/
│       └── tools.py           # Tools for agents (SQL, image viewing)
├── utils/
│   ├── extractor.py           # LangExtract wrapper
│   ├── workers.py             # Worker data models
│   ├── helper_agents.py       # Helper agents for parsing
│   ├── generate_result.py     # Run extraction on assigned rows
│   ├── adapter_factory.py     # Convert worker specs to LangExtract format
│   └── config.yaml            # Master prompt template
├── data/
│   └── prompt_builder.py      # Field specification builder
├── examples/
│   ├── invoice_example1.py    # Invoice extraction example
│   └── document_example.py    # Generic document example
├── tests/
│   └── example_ocr.py         # Test OCR pipeline
├── requirements.txt           # Dependencies
├── LICENSE                    # Apache 2.0
└── README.md                  # This file
```

## Key Concepts

### One Row = One Entity
Due to LangExtract limitations, each database row must contain exactly one complete entity for extraction to work. If a row has multiple entities or is incomplete, the Strategist will recommend Row Builder adjustments.

### Row Structure
Rows in the SQLite database contain:
- `sno`: Sequential row number
- `text`: OCR-extracted text
- `page_no`: Page number (1-based)
- `x_min, y_min, x_max, y_max`: Bounding box coordinates
- `left_margin, right_margin`: Horizontal position (0-1)
- `width_ratio, height_ratio`: Size relative to page dimensions
- `num_fragments`: Count of merged OCR fragments
- `worker`: Assigned worker name

### Worker Definition
```python
{
  "name": "vendor_header_worker",
  "purpose": "Extract vendor company name and address",
  "example_input_row": "Bennett, Coleman And Co. Ltd., 123 Main St",
  "example_output": {
    "company_name": "Bennett, Coleman And Co. Ltd.",
    "address": "123 Main St"
  },
  "validation_rules": [
    "company_name must not be empty",
    "Must contain at least one address component"
  ]
}
```

### Multi-Page Support
The Assigner Agent is designed to:
- Handle documents with repeating structures across pages
- Use anchor-based patterns to identify blocks on each page
- Find ALL instances (not just the first one)
- Verify coverage across all pages

## Configuration

### Agent Models
Configure in `agents/config.yaml`:
- **Strategist**: `gemini-2.5-flash` (fast, good for design)
- **Assigner**: `gemini-2.5-pro` (more reasoning for complex patterns)
- **Reconstructor**: `gemini-2.5-pro` (handles complex grouping)
- **Validator**: `gemini-2.5-pro` (careful validation)
- **RCA**: `gemini-2.5-pro` (detailed analysis)

### Thinking Budgets
Set via configuration for extended reasoning:
```yaml
strategist_config:
  thinking_budget: 4096
  reasoning_max_steps: 250
```

## Advanced Features

### Row Builder Debugging
If the Strategist detects row building issues:
```sql
-- Check for overlapping y-coordinates (split rows)
SELECT sno, text, y_min, y_max 
FROM rows 
WHERE sno BETWEEN (issue_row - 2) AND (issue_row + 2)
```

### Anchor-Based Pattern Matching
For repeating structures:
```sql
WITH start_anchors AS (
  SELECT sno as start_sno, page_no FROM rows WHERE text LIKE '%Total%'
),
end_anchors AS (
  SELECT sno as end_sno, page_no FROM rows WHERE text LIKE '%Page%'
),
paired AS (
  SELECT s.start_sno,
         (SELECT MIN(e.end_sno) FROM end_anchors e
          WHERE e.end_sno > s.start_sno) as end_sno
  FROM start_anchors s
)
SELECT r.* FROM rows r
JOIN paired p ON r.sno > p.start_sno AND r.sno < p.end_sno
```

### Carry-Forward Logic
Items inherit properties from previous rows:
```sql
SELECT 
  sno,
  text,
  page_no,
  COALESCE(
    page_number,
    LAG(page_number) OVER (ORDER BY sno)
  ) as page_number
FROM extractions
```

## Output Format

The Reconstructor produces a `final_output.json` file with your desired structure. Example:

```json
{
  "metadata": {
    "pages": 3,
    "extraction_date": "2024-02-06"
  },
  "vendors": [
    {
      "name": "ACME Corp",
      "invoices": [
        {
          "invoice_number": "INV-001",
          "line_items": [
            {
              "description": "Widget",
              "quantity": 10,
              "price": 5.00
            }
          ],
          "total": 50.00
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Issue: "Extraction fails on rows with 2 entities"
**Solution**: Strategist recommends higher `y_threshold` for Row Builder to merge rows better.

### Issue: "Wrong rows assigned to worker"
**Solution**: 
1. Review `opass.md` (Assigner output)
2. Check if anchor patterns are too broad
3. Validate generalization (does pattern work across all pages?)

### Issue: "Validator reports many failures"
**Solution**:
1. Review `opvals.md` (Validator output)
2. Check if validation rules are too strict
3. Review `oprca.md` (RCA output) for root cause analysis
4. Update worker definitions if needed

### Issue: "Final JSON structure is wrong"
**Solution**:
1. Review `oprec.md` (Reconstructor output)
2. Check if reconstruction logic in `chats.md` is correct
3. Verify grouping SQL logic if custom

## Testing

Run example extraction:
```bash
python examples/invoice_example1.py
```

Check test files:
```bash
python tests/example_ocr.py
```

## Dependencies

Key libraries:
- **agno**: AI agent orchestration framework
- **google-genai**: Google Gemini API
- **openai**: OpenAI API
- **langextract**: Specialized entity extraction
- **SQLAlchemy**: Database ORM
- **Pillow**: Image processing
- **pandas**: Data manipulation
- **pydantic**: Data validation

See [requirements.txt](requirements.txt) for complete list.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with description

## Contact & Support

For issues, questions, or feature requests, please open a GitHub issue.

---

**Built with Gemini AI agents for intelligent document extraction**
