import re
import numpy as np
import pandas as pd
def extract_constraints(query):
    """Extracts constraints using fuzzy pattern detection & word proximity."""
    query = query.lower()
    constraints = {
        "job_level": None,
        "remote_required": None,
        "adaptive_required": None,
        "max_duration": None
    }

    # Duration: extract number before "min" or "minutes"
    duration_match = re.search(r'(\d+)\s*(min|minute)', query)
    if duration_match:
        constraints["max_duration"] = int(duration_match.group(1))

    # Job level: look for word preceding "level" or "position"
    level_match = re.search(r'(\w+)[\s\-]+level', query)
    position_match = re.search(r'(\w+)[\s\-]+position', query)
    job_word = level_match.group(1) if level_match else (position_match.group(1) if position_match else None)
    if job_word:
        job_word = job_word.strip().capitalize()
        # Fuzzy match to known levels
        levels = ["Entry-Level", "Graduate", "Mid-Professional", "Professional Individual Contributor",
                  "Front Line Manager", "Manager", "Supervisor", "Director"]
        similarities = [model.encode(job_word, convert_to_tensor=True) @ model.encode(level, convert_to_tensor=True).T for level in levels]
        best_match = levels[int(np.argmax(similarities))]
        constraints["job_level"] = best_match

    # Remote match
    if any(kw in query for kw in ["remote", "work from home", "virtual"]):
        constraints["remote_required"] = True

    # Adaptive/IRT support
    if any(kw in query for kw in ["adaptive", "irt", "smart test"]):
        constraints["adaptive_required"] = True

    return constraints



def passes_constraints(result, constraints):
    """Return True if assessment satisfies the extracted constraints."""
    # Check job level
    if constraints["job_level"]:
        if constraints["job_level"].lower() not in result.get("Job_levels", "").lower():
            return False
    
    # Check remote
    if constraints["remote_required"] is True:
        if result["Remote_testing_support"].lower() != "yes":
            return False

    # Check adaptive
    if constraints["adaptive_required"] is True:
        if "yes" not in result["Adaptive_IRT_support"].lower():
            return False

    # Check duration
    if constraints["max_duration"]:
        duration = result["Duration_minutes"]
        if pd.isna(duration) or duration > constraints["max_duration"]:
            return False

    return True
