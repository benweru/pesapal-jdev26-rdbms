# Simple RDBMS - PesaPal Junior Dev Challenge '26

## 📌 Overview
This project is a custom implementation of a Relational Database Management System (RDBMS) built from scratch in Python. The goal is to demonstrate core Computer Science fundamentals—specifically Data Structures, File I/O, and Query Parsing—without relying on external database libraries (like SQLite).

**Current Status:** 🚧 In Development (Architecture Phase)

## 🏗 Architecture Design
The database is architected with modularity in mind, separating the user interface from the storage engine.

### 1. The Interface (REPL)
A Read-Eval-Print Loop (REPL) that accepts SQL-like commands from the user.
* **Role:** Input sanitization and display of results.

### 2. The Parser (`src/parser.py`)
A custom lexical analyzer that tokenizes input strings into executable command objects.
* **Supported Syntax (Planned):**
    * `CREATE TABLE`
    * `INSERT INTO`
    * `SELECT * FROM`

### 3. The Storage Engine (`src/database.py`)
Handles data persistence and retrieval.
* **Storage Format:** JSON/CSV files per table.
    * *Design Choice:* While binary files are faster, JSON was chosen for this prototype to allow for human-readable debugging and simpler serialization logic.
* **Indexing:** In-memory Hash Map (Python Dictionary) mapping Primary Keys to file offsets.

## 🗺 Roadmap & Progress
I am following an iterative development approach:

- [x] **Phase 1: System Architecture** (Project Skeleton & Design Doc)
- [ ] **Phase 2: The Storage Layer** (File I/O wrappers)
- [ ] **Phase 3: The Parser** (Tokenizing SQL strings)
- [ ] **Phase 4: Core CRUD Operations** (Insert, Select, Delete)
- [ ] **Phase 5: Advanced Features** (Indexing & Basic Joins)
- [ ] **Phase 6: Web Interface** (Simple Flask App integration)

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Standard Libraries:** `json`, `os`, `csv`, `re` (Regex)
* **Testing:** `unittest`

## 🚀 How to Run
*(Instructions will be updated as modules are completed)*

```bash
python3 src/main.py