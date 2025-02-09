import sqlite3
import os

def execute_query(sql_query: str):
    """
    Executes one or more SQL statements on the SQLite database.

    If the query contains multiple statements (separated by semicolons),
    they are executed as a script. If it's a SELECT query, the results are fetched and returned.
    
    Args:
        sql_query (str): The SQL query (or queries) to execute.

    Returns:
        list: The result set for SELECT queries, or an empty list for non-SELECT queries.

    Raises:
        Exception: If an error occurs during query execution.
    """
    # Determine the absolute path to the database file.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "data", "database.db")
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Split the query on semicolons to see if there are multiple statements.
        # We filter out any empty statements.
        statements = [stmt.strip() for stmt in sql_query.split(';') if stmt.strip()]

        if len(statements) > 1:
            # Multiple statements detected.
            # Rebuild the script with semicolons and execute as a script.
            script = ';'.join(statements) + ';'
            cursor.executescript(script)
            conn.commit()
            # For multi-statement scripts, we assume no results need to be returned.
            return []
        else:
            # Only one statement is present.
            cursor.execute(sql_query)
            # If the statement is a SELECT, fetch and return the results.
            if sql_query.strip().lower().startswith("select"):
                results = cursor.fetchall()
            else:
                conn.commit()
                results = []
            return results

    except Exception as e:
        raise Exception(f"Error executing SQL query: {e}")
    finally:
        if conn:
            conn.close()

# Optional: For standalone testing of the module
if __name__ == "__main__":
    sample_query = """
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INT PRIMARY KEY,
        Name VARCHAR(50),
        Email VARCHAR(100)
    );

    INSERT INTO Customers (CustomerID, Name, Email)
    VALUES
        (1, 'John Doe', 'johndoe@example.com'),
        (2, 'Jane Smith', 'janesmith@example.com');
    """
    try:
        result = execute_query(sample_query)
        print("Query executed successfully. Results:", result)
    except Exception as err:
        print(err)
