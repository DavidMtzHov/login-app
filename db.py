import sqlite3

# Create databases for organization_a and organization_b
db_files = [ 'organization_b.db']
for db_file in db_files:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email) VALUES ('david', 'david@example.com')")
    c.execute("INSERT INTO users (name, email) VALUES ('eugen', 'eugen@example.com')")
    conn.commit()
    conn.close()
