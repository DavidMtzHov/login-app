import sqlite3

# Create databases for organization_a and organization_b
db_files = ['organization_a.db', 'organization_b.db']
db_files = ['user_management.db']
for db_file in db_files:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    c.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    c.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    conn.commit()
    conn.close()
