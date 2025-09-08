import sqlite3

def setup_database():
    # Connect to the database (this will create the file if it doesn't exist)
    conn = sqlite3.connect('database/properties.db')

    # Create a cursor object
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS properties
        (id INTEGER PRIMARY KEY,
         address TEXT,
         city TEXT,
         region TEXT,
         property_type TEXT,
         price INTEGER,
         bedrooms INTEGER,
         bathrooms INTEGER)
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Database and table checked/created successfully.")

if __name__ == '__main__':
    setup_database()
