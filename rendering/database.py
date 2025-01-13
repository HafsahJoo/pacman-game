import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("database.db")
cursor = connection.cursor()


# Create the "user" table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user (
        username TEXT NOT NULL PRIMARY KEY,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0)
"""
)

# Commit the changes and close the connection
connection.commit()
connection.close()
