from typing import List, Dict, Optional, Any
from database.dummy_db import db

class GenericRepository:
    """
    A generic repository for basic CRUD operations on a mock database.
    """
    def __init__(self, table_name: str):
        self.table_name = table_name
        # Ensure the table exists in our mock DB
        if self.table_name not in db:
            db[self.table_name] = []

    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieve all records from the table."""
        return db.get(self.table_name, [])

    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific record by its ID."""
        items = db.get(self.table_name, [])
        for item in items:
            if item.get("id") == item_id:
                return item
        return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record in the table."""
        items = db.get(self.table_name, [])
        # Auto-increment ID based on the max existing ID
        new_id = max([item.get("id", 0) for item in items], default=0) + 1
        data["id"] = new_id
        items.append(data)
        return data

    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing record in the table by its ID."""
        items = db.get(self.table_name, [])
        for index, item in enumerate(items):
            if item.get("id") == item_id:
                # Merge existing item data with new data
                updated_item = {**item, **data, "id": item_id}
                items[index] = updated_item
                return updated_item
        return None

    def delete(self, item_id: int) -> bool:
        """Delete a record from the table by its ID."""
        items = db.get(self.table_name, [])
        for index, item in enumerate(items):
            if item.get("id") == item_id:
                items.pop(index)
                return True
        return False
