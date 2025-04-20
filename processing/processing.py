import json
import re
from pathlib import Path

# Path configuration
RAW_FILE = Path("shl_assessments.json")              # Input from your spider
PROCESSED_JSON = Path("processed_shl_assessments.json")  # Output file

# Mapping short test types to descriptive labels
TEST_TYPE_LABELS = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

def parse_duration(text):
    """Extract duration in minutes from raw string"""
    if not text:
        return None
    # Check after the '=' sign for the duration of the assessment
    match = re.search(r'=\s*(\d+)', text)
    if match:
        return int(match.group(1))
    match = re.search(r'(\d+)\s*min', text, re.IGNORECASE)
    return int(match.group(1)) if match else None

def process_entry(entry):
    """Convert one raw entry to a cleaned, structured format"""
    test_types = entry.get("test_types", [])
    mapped_types = [TEST_TYPE_LABELS.get(t.strip(), t) for t in test_types]

    # Handle boolean flags
    remote = entry.get("remote_testing", "").lower().strip() == "yes"
    adaptive = "yes" in entry.get("adaptive_supported", "").lower()

    # Build embedding text
    parts = [
        entry.get("description", "").strip(),
        f"Applicable job levels: {entry.get('job_levels', 'Not specified')}",
        f"Available languages: {entry.get('languages', 'Not specified')}",
        f"Test duration: {parse_duration(entry.get('duration_minutes', '')) or 'Unknown'} minutes",
        f"Measures: {', '.join(mapped_types)}" if mapped_types else "",
        f"Remote testing available: {'Yes' if remote else 'No'}",
        f"Adaptive testing: {'Supported' if adaptive else 'Not supported'}"
    ]

    return {
        "Assessment_name": entry.get("title", "").strip(),
        "URL": entry.get("url", "").strip(),
        "Description": entry.get("description", "").strip(),
        "Job_levels": entry.get("job_levels", "").strip().rstrip(","),
        "Languages": entry.get("languages", "").strip().rstrip(","),
        "Duration_minutes": parse_duration(entry.get("duration_minutes", "")),
        "Test_types": mapped_types,
        "Remote_testing_support": 'Yes' if remote else 'No',
        "Adaptive_IRT_support": 'Supported' if adaptive else 'Not supported',
        "embedding_text": ". ".join(parts)
    }

def main():
    # Load raw scraped data
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # Process each entry
    processed_data = [process_entry(entry) for entry in raw_data]

    # Save output
    with open(PROCESSED_JSON, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Processed {len(processed_data)} entries and saved to {PROCESSED_JSON}")

if __name__ == "__main__":
    main()
