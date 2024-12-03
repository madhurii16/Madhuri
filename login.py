from flask_bcrypt import Bcrypt
import sqlite3

# Initialize Bcrypt
bcrypt = Bcrypt()

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Fetch all users and their current passwords
cursor.execute("SELECT user_id, password FROM users")
users = cursor.fetchall()

# Loop through each user
for user in users:
    user_id, current_password = user

    # Check if the password is already hashed (bcrypt hashes start with "$2b$")
    if not current_password.startswith("$2b$"):
        # Hash the plain text password
        hashed_password = bcrypt.generate_password_hash(current_password).decode('utf-8')

        # Update the password in the database
        cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (hashed_password, user_id))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Passwords successfully hashed!")
