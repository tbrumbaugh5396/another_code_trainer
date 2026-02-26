import sqlite3

def init_db():
    conn = sqlite3.connect("trainer.db")
    # Using a structured schema
    conn.execute("""CREATE TABLE IF NOT EXISTS problems 
                 (id INTEGER PRIMARY KEY, 
                  title TEXT, 
                  description TEXT, 
                  input_output TEXT,
                  prerequisites TEXT, 
                  complexity_time TEXT,
                  complexity_space TEXT,
                  code_snippets TEXT,
                  source TEXT)""")
    conn.close()

if __name__ == "__main__":
    init_db()
