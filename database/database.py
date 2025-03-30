import json
import os
from datetime import datetime

from tinydb import Query, TinyDB


class Database:
    def __init__(self, db_path="data/db.json"):
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Initialize database
        self.db = TinyDB(db_path)
        self.query = Query()

    def set(self, key, value):
        """Store a value with a key"""
        # Convert set to list before JSON serialization
        if isinstance(value, set):
            value = list(value)

        # Handle datetime first
        if isinstance(value, datetime):
            value = value.isoformat()
        # Then handle other non-string types with JSON
        elif not isinstance(value, str):
            value = json.dumps(value)

        # Update or insert the value
        self.db.upsert({"key": key, "value": value}, self.query.key == key)

    def set_if_not_exists(self, key, value):
        """Store a value with a key if it doesn't exist"""
        if not self.exists(key):
            self.set(key, value)
            
    def get(self, key, default=None):
        """Retrieve a value by key"""
        result = self.db.get(self.query.key == key)
        if result:
            try:
                # Try to parse as JSON if it's a JSON string
                value = json.loads(result["value"])
                # Convert ISO datetime strings to datetime objects
                try:
                    return datetime.fromisoformat(value)
                except (TypeError, ValueError):
                    return value
            except:
                # Return as string if not JSON
                # Try to convert string to datetime
                try:
                    return datetime.fromisoformat(result["value"])
                except (TypeError, ValueError):
                    return result["value"]
        return default

    def delete(self, key):
        """Delete a key-value pair"""
        self.db.remove(self.query.key == key)

    def exists(self, key):
        """Check if a key exists"""
        return self.db.contains(self.query.key == key)

    def clear(self):
        """Clear all data"""
        self.db.truncate()