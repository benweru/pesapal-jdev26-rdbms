import re
from typing import Union, List, Dict, Any, Optional
from database import Table

def parse_command(query: str) -> Union[str, List[Dict[str, Any]]]:
    """
    Parses and executes a SQL-like command.
    
    Supported syntax:
    - CREATE TABLE table_name (col1, col2, ...)
    - INSERT INTO table_name (col1, col2, ...) VALUES (val1, val2, ...)
    - SELECT * FROM table_name
    
    Args:
        query (str): The SQL command string.
        
    Returns:
        Union[str, List[Dict[str, Any]]]: A status message string or a list of rows (for SELECT).
    """
    query = query.strip()
    
    # 1. CREATE TABLE
    # Example: CREATE TABLE users (id INT, name STRING)
    create_pattern = r"^CREATE\s+TABLE\s+(\w+)\s*\((.+)\)$"
    create_match = re.match(create_pattern, query, re.IGNORECASE)
    
    if create_match:
        table_name = create_match.group(1)
        columns_str = create_match.group(2)
        
        # Parse columns and optional types
        # Input: "id INT, name STRING" -> output schema: {"id": "INT", "name": "STRING"}
        # Input: "id, name" -> output schema: {} (backward compatibility)
        schema = {}
        columns = []
        
        raw_cols = [c.strip() for c in columns_str.split(',')]
        for raw_c in raw_cols:
            parts = raw_c.split()
            col_name = parts[0]
            columns.append(col_name)
            if len(parts) > 1:
                schema[col_name] = parts[1]
        
        Table(table_name, schema=schema)
        return f"Table '{table_name}' created with columns: {columns} (Schema: {schema})"

    # 2. INSERT INTO
    # Example: INSERT INTO users (id, name) VALUES (1, 'Alice')
    insert_pattern = r"^INSERT\s+INTO\s+(\w+)\s*\((.+)\)\s*VALUES\s*\((.+)\)$"
    insert_match = re.match(insert_pattern, query, re.IGNORECASE)
    
    if insert_match:
        table_name = insert_match.group(1)
        columns_str = insert_match.group(2)
        values_str = insert_match.group(3)
        
        cols = [c.strip() for c in columns_str.split(',')]
        
        # Simple CSV-style splitting for values. 
        # Note: This basic split doesn't strictly handle commas inside quoted strings.
        vals = [v.strip().strip("'").strip('"') for v in values_str.split(',')]
        
        if len(cols) != len(vals):
            return f"Error: Column count ({len(cols)}) does not match value count ({len(vals)})."
        
        # Construct the row dictionary
        row_data = dict(zip(cols, vals))
        
        table = Table(table_name)
        table.save_row(row_data)
        return f"Inserted 1 row into '{table_name}'."

    # 3. SELECT * FROM
    # Example: SELECT * FROM users
    select_pattern = r"^SELECT\s+\*\s+FROM\s+(\w+)$"
    select_match = re.match(select_pattern, query, re.IGNORECASE)
    
    if select_match:
        table_name = select_match.group(1)
        table = Table(table_name)
        rows = table.load_rows()
        return rows

    # 4. DELETE FROM
    # Example: DELETE FROM users WHERE id=1
    delete_pattern = r"^DELETE\s+FROM\s+(\w+)\s+WHERE\s+(\w+)\s*=\s*(.+)$"
    delete_match = re.match(delete_pattern, query, re.IGNORECASE)
    
    if delete_match:
        table_name = delete_match.group(1)
        # col_name = delete_match.group(2) # Not strictly used in simple delete_row impl which assumes PK
        val = delete_match.group(3).strip().strip("'").strip('"')
        
        table = Table(table_name)
        if table.delete_row(val):
            return f"Deleted row with PK={val} from '{table_name}'."
        else:
            return f"Error: Row with PK={val} not found in '{table_name}'."

    # 5. UPDATE
    # Example: UPDATE users SET name='Bob', email='bob@test.com' WHERE id=1
    update_pattern = r"^UPDATE\s+(\w+)\s+SET\s+(.+)\s+WHERE\s+(\w+)\s*=\s*(.+)$"
    update_match = re.match(update_pattern, query, re.IGNORECASE)
    
    if update_match:
        table_name = update_match.group(1)
        assignments_str = update_match.group(2)
        # col_name = update_match.group(3) # Assume PK
        pk_val = update_match.group(4).strip().strip("'").strip('"')
        
        table = Table(table_name)
        rows = table.load_rows()
        target_row = None
        
        # Find existing row
        for r in rows:
            # Check First Column as PK
            if str(list(r.values())[0]) == pk_val:
                target_row = r
                break
        
        if not target_row:
            return f"Error: Row with PK={pk_val} not found in '{table_name}'."
            
        # Parse assignments: name='Bob', email='bob@test.com'
        # Simple split by comma (warning: doesn't handle quoted commas well)
        assigns = [a.strip() for a in assignments_str.split(',')]
        for a in assigns:
            if '=' in a:
                key, val = a.split('=', 1)
                key = key.strip()
                val = val.strip().strip("'").strip('"')
                target_row[key] = val
        
        # Save update
        table.update_row(pk_val, target_row)
        return f"Updated row PK={pk_val} in '{table_name}'."

    return "Error: Unknown command or syntax error."
