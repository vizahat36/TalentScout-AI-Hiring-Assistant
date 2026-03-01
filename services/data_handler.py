"""
Create a data handler for storing candidate data.

Requirements:
- Save candidate info to data/candidates.json
- Append new entries
- Handle file not found safely
- Use proper exception handling
- Add docstrings
"""
import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "candidates.json")


def save_candidate_data(candidate_data: dict):
    """
    Saves candidate data to JSON file.
    Appends new candidate to existing list.
    
    Args:
        candidate_data: Dictionary containing candidate information
    """

    try:
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Ensure file exists
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

        # Load existing data
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        # Add timestamp to candidate data
        candidate_data["timestamp"] = datetime.now().isoformat()
        
        # Append new candidate
        data.append(candidate_data)

        # Save updated data
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"✓ Candidate data saved successfully to {DATA_FILE}")

    except Exception as e:
        print(f"Data Save Error: {e}")
