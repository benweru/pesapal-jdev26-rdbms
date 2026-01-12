from flask import Flask, render_template, request, redirect, url_for, flash
from database import Table
import os

app = Flask(__name__)
# Secret key required for session/flash messages
app.secret_key = 'pesapal-secret-key-challenge-2026'

DATA_DIR = "data"

def get_tables():
    """Returns a list of available table names (based on .json files)."""
    if not os.path.exists(DATA_DIR):
        return []
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    # Strip extension
    return [f[:-5] for f in files]

@app.route('/')
def index():
    tables = get_tables()
    
    # Determine current table
    # Default to 'users' if available, otherwise first table, otherwise None
    default_table = 'users' if 'users' in tables else (tables[0] if tables else None)
    current_table_name = request.args.get('table', default_table)
    
    rows = []
    columns = []
    
    if current_table_name:
        table = Table(current_table_name)
        rows = table.load_rows()
        
        # Sort by ID if possible
        try:
            rows.sort(key=lambda x: int(list(x.values())[0])) # Assume first col is ID/PK
        except:
            pass
            
        # Infer columns from first row if exists
        # NOTE: If table is empty, we won't know columns yet.
        if rows:
            columns = list(rows[0].keys())
            
    return render_template('index.html', 
                           tables=tables, 
                           current_table=current_table_name, 
                           rows=rows, 
                           columns=columns)

@app.route('/add_row', methods=['POST'])
def add_row():
    table_name = request.form.get('table_name')
    if not table_name:
        flash("Unknown table.", "error")
        return redirect(url_for('index'))
    
    # Collect form data, excluding the table_name hidden field
    row_data = {k: v for k, v in request.form.items() if k != 'table_name'}
    
    if row_data:
        try:
            table = Table(table_name)
            table.save_row(row_data)
            flash(f"Row added to '{table_name}' successfully!", "success")
        except ValueError as e:
            flash(f"Error: {e}", "error")
            
    return redirect(url_for('index', table=table_name))

@app.route('/edit_row/<table_name>/<pk>')
def edit_row(table_name, pk):
    table = Table(table_name)
    rows = table.load_rows()
    
    # Find row by PK (assuming first column is PK)
    target_row = None
    for r in rows:
        if str(list(r.values())[0]) == str(pk):
            target_row = r
            break
            
    if target_row:
        return render_template('edit_user.html', row=target_row, table_name=table_name) # Reusing edit_user.html as edit_row template
    else:
        flash(f"Row #{pk} not found in '{table_name}'.", "error")
        return redirect(url_for('index', table=table_name))

@app.route('/update_row', methods=['POST'])
def update_row():
    table_name = request.form.get('table_name')
    original_pk = request.form.get('original_pk') # To identify the row
    
    # Collect new data
    new_data = {k: v for k, v in request.form.items() if k not in ['table_name', 'original_pk']}
    
    # We need the PK of the new data to call update_row
    # Assuming first key of new_data is the PK
    if new_data:
        pk_val = list(new_data.values())[0] 
        # Ideally, we trust original_pk if we want to allow PK updates, 
        # but our simple DB uses PK as index.
        # Let's use the original_pk to find and update.
        
        table = Table(table_name)
        if table.update_row(original_pk, new_data):
            flash(f"Row updated successfully.", "success")
        else:
            flash(f"Update failed.", "error")
            
    return redirect(url_for('index', table=table_name))

@app.route('/delete_row', methods=['POST'])
def delete_row():
    table_name = request.form.get('table_name')
    pk = request.form.get('pk')
    
    if table_name and pk:
        table = Table(table_name)
        if table.delete_row(pk):
            flash(f"Row #{pk} deleted.", "success")
        else:
            flash(f"Row #{pk} not found.", "error")
            
    return redirect(url_for('index', table=table_name))

if __name__ == '__main__':
    print("Starting Flask App connecting to BenDB...")
    app.run(debug=True, port=5000)
