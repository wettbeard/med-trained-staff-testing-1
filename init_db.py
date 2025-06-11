import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'nurse', 'viewer')),
    company_id INTEGER NOT NULL
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS HCP (
    hcp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    company_id INTEGER NOT NULL
)
''')

# Sample users
conn.execute("INSERT OR IGNORE INTO Users (username, password_hash, role, company_id) VALUES (?, ?, ?, ?)",
             ('admin', generate_password_hash('admin123'), 'admin', 1))
conn.execute("INSERT OR IGNORE INTO Users (username, password_hash, role, company_id) VALUES (?, ?, ?, ?)",
             ('nurse1', generate_password_hash('nurse123'), 'nurse', 2))
conn.execute("INSERT OR IGNORE INTO Users (username, password_hash, role, company_id) VALUES (?, ?, ?, ?)",
             ('viewer1', generate_password_hash('viewer123'), 'viewer', 3))

# Sample HCPs
conn.execute("INSERT OR IGNORE INTO HCP (name, company_id) VALUES (?, ?)", ('Alice Brown', 2))
conn.execute("INSERT OR IGNORE INTO HCP (name, company_id) VALUES (?, ?)", ('Bob Smith', 3))
conn.execute("INSERT OR IGNORE INTO HCP (name, company_id) VALUES (?, ?)", ('Charlie Day', 2))

conn.commit()
conn.close()
