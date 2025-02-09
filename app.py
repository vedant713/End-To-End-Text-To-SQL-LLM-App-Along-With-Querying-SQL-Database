import streamlit as st
from llm import text_to_sql  # Function that converts text to SQL query
from database import execute_query  # Function that executes SQL query on the database

# Set page configuration
st.set_page_config(
    page_title="Text-to-SQL Converter App ⚡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS and emojis for an enhanced UI
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f9f9f9;
    }
    .css-18e3th9 {
        font-size: 2.5rem;
        font-weight: 600;
        color: #333;
    }
    div.stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #155a8a;
    }
    textarea {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.sidebar.header("ℹ️ Instructions")
    st.sidebar.info(
        "Welcome to the **Text-to-SQL Converter App**! 🤖\n\n"
        "1. Enter any text in the input box. 📝\n"
        "2. Click **Convert and Execute** to generate an SQL query. ⚡️\n"
        "3. If the generated query does not contain typical SQL keywords, you can review and optionally execute it. 🚀"
    )

    st.title("Text-to-SQL Converter App 🚀")
    st.markdown("Convert any natural language input into an SQL query effortlessly! 💡")

    user_query = st.text_area(
        "Enter your query here:",
        height=150,
        placeholder="E.g., 'Show me the top 10 customers by total purchase amount.' or 'Create table of customer'"
    )

    if st.button("Convert and Execute 🔄"):
        if not user_query.strip():
            st.warning("⚠️ Please enter a valid query.")
            return

        # Convert the input text to SQL using the LLM
        with st.spinner("🧠 Converting text to SQL query..."):
            try:
                sql_query = text_to_sql(user_query)
            except Exception as e:
                st.error(f"❌ Error during text-to-SQL conversion: {e}")
                return

        # Validate the generated SQL
        if sql_query.startswith("INVALID:"):
            st.error(f"❌ {sql_query}")
            return

        # Expanded list of SQL keywords to cover DML and DDL commands
        valid_keywords = [
            "select", "create", "insert", "update", "delete", "alter",
            "drop", "truncate", "merge", "explain", "with", "show", "rename"
        ]

        # Check if at least one valid SQL keyword is present (case-insensitive)
        if not any(kw in sql_query.lower() for kw in valid_keywords):
            st.info("⚠️ The generated query does not contain any typical SQL keywords. Please review it below:")
            st.code(sql_query, language="sql")
            if st.button("Execute Query Anyway"):
                with st.spinner("⏳ Executing SQL query on the database..."):
                    try:
                        results = execute_query(sql_query)
                        st.subheader("Query Results 📊")
                        if results:
                            st.write(results)
                        else:
                            st.info("ℹ️ The query executed successfully, but no results were returned.")
                    except Exception as e:
                        st.error(f"❌ Error executing SQL query: {e}")
            return

        st.subheader("Generated SQL Query 📜")
        st.code(sql_query, language="sql")

        # Execute the SQL query on the database
        with st.spinner("⏳ Executing SQL query on the database..."):
            try:
                results = execute_query(sql_query)
            except Exception as e:
                st.error(f"❌ Error executing SQL query: {e}")
                return

        st.subheader("Query Results 📊")
        if results:
            st.write(results)
        else:
            st.info("ℹ️ The query executed successfully, but no results were returned.")

if __name__ == "__main__":
    main()
