import streamlit as st
from llm import text_to_sql  # Function that converts text to SQL query
from database import execute_query  # Function that executes SQL query on the database

def main():
    st.title("Text-to-SQL Converter App")
    st.write("Enter a natural language query to generate and execute an SQL query.")

    # Text input for the natural language query
    user_query = st.text_area("Enter your query here:")

    if st.button("Convert and Execute"):
        if not user_query.strip():
            st.warning("Please enter a valid query.")
            return

        # Convert the natural language query to SQL using the LLM
        st.info("Converting text to SQL query...")
        try:
            sql_query = text_to_sql(user_query)
            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")
        except Exception as e:
            st.error(f"Error during text-to-SQL conversion: {e}")
            return

        # Execute the generated SQL query on the database
        st.info("Executing SQL query on the database...")
        try:
            results = execute_query(sql_query)
            st.subheader("Query Results")
            if results:
                st.write(results)
            else:
                st.info("The query executed successfully, but no results were returned.")
        except Exception as e:
            st.error(f"Error executing SQL query: {e}")

if __name__ == "__main__":
    main()
