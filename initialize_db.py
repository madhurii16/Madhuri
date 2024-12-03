import sqlite3

def initialize_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            role TEXT CHECK(role IN ('user', 'admin')) DEFAULT 'user'
        );
    ''')

    # Create E-Waste Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS e_waste_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            base_price REAL NOT NULL
        );
    ''')

    # Create Collection Spots table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collection_spots (
            spot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_name TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            contact TEXT
        );
    ''')

    # Create Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            condition TEXT CHECK(condition IN ('Excellent', 'Good', 'Fair', 'Poor')) NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (item_id) REFERENCES e_waste_items(item_id)
        );
    ''')

    # Create Admins table (Optional)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    ''')

                            # Insert initial data
                            cursor.executemany('''
                                INSERT INTO e_waste_items (item_name, base_price) VALUES (?, ?)
                            ''', [
                                ('Laptop', 5000),
                                ('Smartphone', 3000),
                                ('Television', 7000),
                                ('Refrigerator', 10000),
                                ('Washing Machine', 8000)
                            ])

                            cursor.executemany('''
                                INSERT INTO collection_spots (spot_name, address, city, state, contact) VALUES (?, ?, ?, ?, ?)
                            ''', [
                                ('Green Tech Recycling', '123 Green Lane', 'New York', 'NY', '123-456-7890'),
                                ('EcoDrop Center', '456 Recycle Road', 'San Francisco', 'CA', '987-654-3210')
                            ])

    # Commit and close
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_db()
