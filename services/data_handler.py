"""
Data Handler for managing candidate data
"""
import json
import os
from datetime import datetime
from config.settings import Settings

class DataHandler:
    """Handles data persistence for candidates"""
    
    def __init__(self):
        self.settings = Settings()
        self.candidates_file = self.settings.CANDIDATES_FILE
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(self.settings.DATA_DIR, exist_ok=True)
        
        # Create candidates file if it doesn't exist
        if not os.path.exists(self.candidates_file):
            with open(self.candidates_file, 'w') as f:
                json.dump({"candidates": []}, f, indent=2)
    
    def save_candidate(self, candidate_data: dict):
        """
        Save candidate data to JSON file
        
        Args:
            candidate_data: Dictionary containing candidate information
        """
        # Add timestamp
        candidate_data['timestamp'] = datetime.now().isoformat()
        
        # Load existing data
        data = self.load_all_candidates()
        
        # Add new candidate
        data['candidates'].append(candidate_data)
        
        # Save to file
        with open(self.candidates_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_all_candidates(self) -> dict:
        """Load all candidates from JSON file"""
        try:
            with open(self.candidates_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"candidates": []}
    
    def get_candidate_by_name(self, name: str) -> dict:
        """Get candidate data by name"""
        data = self.load_all_candidates()
        for candidate in data['candidates']:
            if candidate.get('name', '').lower() == name.lower():
                return candidate
        return None
    
    def get_candidates_by_position(self, position: str) -> list:
        """Get all candidates for a specific position"""
        data = self.load_all_candidates()
        return [c for c in data['candidates'] 
                if c.get('position', '').lower() == position.lower()]
    
    def delete_candidate(self, name: str) -> bool:
        """Delete a candidate by name"""
        data = self.load_all_candidates()
        initial_count = len(data['candidates'])
        
        data['candidates'] = [c for c in data['candidates'] 
                             if c.get('name', '').lower() != name.lower()]
        
        if len(data['candidates']) < initial_count:
            with open(self.candidates_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        return False
