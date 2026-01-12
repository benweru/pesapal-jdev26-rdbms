from typing import List, Dict, Any
from database import Table

def nested_loop_join(table1_name: str, table2_name: str, on_column: str) -> List[Dict[str, Any]]:
    """
    Performs a simple INNER JOIN on two tables using the Nested-Loop Join algorithm.
    
    Args:
        table1_name (str): The name of the first table (Left).
        table2_name (str): The name of the second table (Right).
        on_column (str): The column name to join on (must exist in both tables).
        
    Returns:
        List[Dict[str, Any]]: A list of merged rows where the join condition matches.
    """
    t1 = Table(table1_name)
    t2 = Table(table2_name)
    
    t1_rows = t1.load_rows()
    t2_rows = t2.load_rows()
    
    results = []
    
    # Nested-Loop Join: O(N * M) complexity
    for r1 in t1_rows:
        for r2 in t2_rows:
            # Check if both rows have the join column and values match
            if on_column in r1 and on_column in r2:
                if r1[on_column] == r2[on_column]:
                    # Merge rows. 
                    # specific collision handling: 
                    # If columns have same name (other than join col), 
                    # the right table (r2) will overwrite left table (r1) in this simple dict merge.
                    # For a robust DB, we'd prefix columns (e.g. table1.id, table2.id).
                    # But for this simple challenge, we'll just merge.
                    merged_row = {**r1, **r2} 
                    results.append(merged_row)
                    
    return results
