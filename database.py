import sqlite3
import os

def execute_query(sql_query: str):
    """
    Executes the given SQL query on the SQLite database.

    Args:
        sql_query (str): The SQL query to execute.

    Returns:
        list: The result set of the query as a list of tuples for SELECT queries,
              or an empty list for non-SELECT queries.

    Raises:
        Exception: If an error occurs during query execution.
    """
    # Determine the absolute path to the database file.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "data", "database.db")
    
    try:
        # Connect to the SQLite database.
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute the SQL query.
        cursor.execute(sql_query)

        # If the query is a SELECT statement, fetch the results.
        if sql_query.strip().lower().startswith("select"):
            results = cursor.fetchall()
        else:
            # For other queries (e.g., INSERT, UPDATE, DELETE), commit changes.
            conn.commit()
            results = []

        return results
    except Exception as e:
        raise Exception(f"Error executing SQL query: {e}")
    finally:
        # Ensure the database connection is closed.
        if conn:
            conn.close()


# Optional: For standalone testing of the module
if __name__ == "__main__":
    sample_query = "SELECT sqlite_version();"
    try:
        result = execute_query(sample_query)
        print("Query Results:", result)
    except Exception as err:
        print(err)
