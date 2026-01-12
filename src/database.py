import json
import os
from typing import List, Dict, Any

class Table:
    """
    Represents a database table managed via a JSON file.
    
    Attributes:
        name (str): The name of the table.
        file_path (str): The absolute path to the JSON storage file.
    """
    
    DB_FOLDER = "data"

    def __init__(self, table_name: str, schema: Dict[str, str] = None):
        """
        Initialize the Table instance.
        
        Args:
            table_name (str): The name of the table (used for the filename).
            schema (Dict[str, str]): Optional dictionary of {column: type}. 
                                     E.g., {"id": "int", "name": "str"}
        """
        self.name = table_name
        self.schema = schema or {}
        
        # Ensure the data directory exists
        if not os.path.exists(self.DB_FOLDER):
            os.makedirs(self.DB_FOLDER)
            
        self.file_path = os.path.join(self.DB_FOLDER, f"{table_name}.json")
        
        # Initialize the file if it doesn't exist
        if not os.path.exists(self.file_path):
            self._write_file([])
            
        # 3. Indexing: Load Primary Keys into memory
        self.primary_keys = set()
        self._build_index()

    def _build_index(self) -> None:
        """
        Reads the file and populates the primary_keys set.
        Assumption: The first key in the JSON object is the Primary Key.
        """
        rows = self.load_rows()
        for row in rows:
            if row:
                # Get the first key's value as the PK
                pk_val = list(row.values())[0]
                self.primary_keys.add(str(pk_val))

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """
        Internal helper to write the list of rows to the JSON file.
        
        Args:
            data (List[Dict[str, Any]]): The data to write.
        """
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def delete_row(self, pk_value: Any) -> bool:
        """
        Deletes a row by its Primary Key.
        
        Args:
            pk_value (Any): The primary key of the row to delete.
            
        Returns:
            bool: True if deleted, False if not found.
        """
        pk_str = str(pk_value)
        if pk_str not in self.primary_keys:
            return False
            
        current_data = self.load_rows()
        # Filter out the row with the matching PK (assumed to be first col)
        new_data = [row for row in current_data if str(list(row.values())[0]) != pk_str]
        
        self._write_file(new_data)
        self.primary_keys.remove(pk_str)
        print(f"[DEBUG] Deleted row PK={pk_str} from {self.name}")
        return True

    def update_row(self, pk_value: Any, new_data: Dict[str, Any]) -> bool:
        """
        Updates a row by its Primary Key.
        
        Args:
            pk_value (Any): The primary key of the row to update.
            new_data (Dict[str, Any]): The new data dictionary.
            
        Returns:
            bool: True if updated, False if not found.
        """
        pk_str = str(pk_value)
        if pk_str not in self.primary_keys:
            return False
            
        # Ensure the PK hasn't changed, or if it has, handle it (for now, assume PK immutable or handled upstream)
        # But simple check: ensure new_data has same PK
        
        current_data = self.load_rows()
        updated = False
        final_data = []
        
        for row in current_data:
            # Check if this is the row to update
            if str(list(row.values())[0]) == pk_str:
                # Update logic: we replace the row entirely with new_data
                # OR we could merge. Let's replace for simplicity but ensure keys match schema if strict.
                final_data.append(new_data)
                updated = True
            else:
                final_data.append(row)
        
        if updated:
            self._write_file(final_data)
            print(f"[DEBUG] Updated row PK={pk_str} in {self.name}")
            return True
        return False

    def save_row(self, row_data: Dict[str, Any]) -> None:
        """
        Appends a new row of data to the table's JSON file.
        
        Args:
            row_data (Dict[str, Any]): A dictionary representing the row columns and values.
        
        Raises:
            ValueError: If the Primary Key already exists.
        """
        # Constraint Check: PK Uniqueness
        if not row_data:
            return

        pk_val = str(list(row_data.values())[0])
        
        if pk_val in self.primary_keys:
            raise ValueError(f"Duplicate Primary Key '{pk_val}'")
            
        current_data = self.load_rows()
        current_data.append(row_data)
        self._write_file(current_data)
        
        # Update in-memory index
        self.primary_keys.add(pk_val)
        print(f"[DEBUG] Saved row to {self.name}: {row_data}")

    def load_rows(self) -> List[Dict[str, Any]]:
        """
        Reads all rows from the table's JSON file.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a row.
        """
        if not os.path.exists(self.file_path):
            return []
            
        try:
            with open(self.file_path, 'r') as f:
                # Handle empty files or JSON errors gracefully
                content = f.read()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            return []
