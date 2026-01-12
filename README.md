# RDBMS by Benweru - Custom RDBMS (PesaPal Challenge '26)

## 📌 Overview
This project is a custom implementation of a **Relational Database Management System (RDBMS)** built from scratch in Python. It demonstrates core Computer Science fundamentals—Data Structures, File I/O, Query Parsing, and Relational Algebra—without relying on external database libraries (like SQLite or SQLAlchemy).

It includes a **CLI REPL** for direct SQL interaction and a **Flask Web App** to demonstrate CRUD operations visually.

**Current Status:** ✅ Completed

## 🚀 Features
*   **Custom Storage Engine**: Data persistence using JSON files (one per table).
*   **SQL Parser**: Supports a subset of SQL:
    *   `CREATE TABLE users (id INT, name STRING)`
    *   `INSERT INTO users (id, name) VALUES (1, 'Alice')`
    *   `SELECT * FROM users`
    *   `UPDATE users SET name='Bob' WHERE id=1`
    *   `DELETE FROM users WHERE id=1`
*   **Indexing**: In-memory Hash Map (Python `set`) for **Primary Key** enforcement (O(1) lookup).
*   **Dynamic Table Management**: The Web Dashboard automatically scans and manages *any* table created via CLI, offering a dynamic UI for all data.
*   **Relational Logic**: Supports **Nested-Loop Joins** to combine data from multiple tables.
*   **Web Interface**: A modern, glassmorphism-styled Web Dashboard built with Flask.

## 🛠 Tech Stack
*   **Language:** Python 3.10+
*   **Web Framework:** Flask (only for the UI layer)
*   **Storage:** Native JSON / CSV
*   **Testing:** `unittest` and manual CLI verification

## 📦 Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/benweru/pesapal-jdev26-rdbms.git
    cd pesapal-jdev26-rdbms
    ```

2.  **Install Dependencies** (only Flask is required):
    ```bash
    pip install flask
    ```

## �️ How to Run

### Option 1: The Web Application (Recommended)
Launch the visual dashboard to manage your database.

```bash
python src/app.py
```
*   Open your browser to `http://127.0.0.1:5000/`.
*   You can **Add**, **View**, **Edit**, and **Delete** users via the UI.

### Option 2: The CLI REPL
Interact directly with the database engine using SQL commands.

```bash
python src/main.py
```
**Example Commands:**
```sql
CREATE TABLE students (id, name)
INSERT INTO students (id, name) VALUES (1, 'Allan')
SELECT * FROM students
```

## 🏗 Architecture
1.  **`src/database.py`**: The Storage Engine. Handles file I/O, `Table` class, schemas, and `save/load/delete/update` operations.
2.  **`src/parser.py`**: The Lexer. Tokenizes strings using Regex and executes commands.
3.  **`src/joins.py`**: Implements the Nested-Loop Join algorithm.
4.  **`src/app.py`**: The Flask Controller connecting the Web UI to the Custom DB.
