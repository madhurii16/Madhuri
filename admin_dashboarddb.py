import sqlite3

DATABASE = 'database.db'  # Path to your SQLite database file

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To access rows like dictionaries
    return conn

def get_total_spots():
    conn = get_db_connection()
    total = conn.execute('SELECT COUNT(*) FROM collection_spots').fetchone()[0]
    conn.close()
    return total
def get_total_e_waste():
    conn = get_db_connection()
    total = conn.execute('SELECT SUM(quantity) FROM transactions').fetchone()[0]
    conn.close()
    return total if total else 0  # Handle case where no data exists

def get_total_users():
    conn = get_db_connection()
    total = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    conn.close()
    return total

def get_collection_spots():
    conn = get_db_connection()
    spots = conn.execute('SELECT * FROM collection_spots').fetchall()
    conn.close()
    return spots

def get_e_waste_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM e_waste_items').fetchall()
    conn.close()
    return items
