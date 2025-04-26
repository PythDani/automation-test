import sqlite3

def create_db():
    """
    Creates a SQLite database and a table to store test results.

    This function connects to a SQLite database named 'test_results.db'.
    If the database does not exist, it will be created. A table named
    'test_results' is created if it does not already exist, with columns
    for storing the ID, test name, result, and a timestamp of when the
    result was recorded.

    The table schema is as follows:
    - id: INTEGER PRIMARY KEY
    - test_name: TEXT
    - result: TEXT
    - timestamp: DATETIME with default value as the current timestamp

    After creating the table, the database connection is committed and closed.
    """

    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY,
        test_name TEXT,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()        

def store_result(test_name, result):
    """
    Stores a test result in the 'test_results' SQLite database.

    This function inserts a new record into the 'test_results' table with
    the given test name and result. The timestamp of when the result is
    recorded is automatically set to the current time.

    Parameters:
    - test_name (str): The name of the test.
    - result (str): The result of the test, e.g., 'passed', 'failed'.

    After inserting the record, the database connection is committed and closed.
    """

    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()
    
    # Insert results into the database
    cursor.execute('''
    INSERT INTO test_results (test_name, result)
    VALUES (?, ?)
    ''', (test_name, result))
    
    conn.commit()
    conn.close()