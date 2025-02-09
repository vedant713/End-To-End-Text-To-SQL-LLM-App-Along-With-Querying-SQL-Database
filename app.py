import streamlit as st
from llm import text_to_sql  # Function that converts text to SQL query
from database import execute_query  # Function that executes SQL query on the database

# Set the page configuration
st.set_page_config(
    page_title="Text-to-SQL Converter ⚡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance UI appearance
st.markdown(
    """
    <style>
    /* Overall background styling */
    .reportview-container {
        background: #f9f9f9;
    }
    /* Title styling */
    .css-18e3th9 {
        font-size: 2.5rem;
        font-weight: 600;
        color: #333;
    }
    /* Button styling */
    div.stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #155a8a;
    }
    /* Text area styling */
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
    # Sidebar for instructions with emojis
    st.sidebar.header("ℹ️ Instructions")
    st.sidebar.info(
        "Welcome to the **Text-to-SQL Converter App**! 🤖\n\n"
        "1. **Enter your natural language query** in the text area. 📝\n"
        "2. Click **Convert and Execute** to generate the corresponding SQL query. ⚡️\n"
        "3. The app will display the generated SQL query and execute it against the database. 📊\n\n"
        "Enjoy exploring your data with this tool! 🚀"
    )

    # Main title and description with emoji
    st.title("Text-to-SQL Converter App 🚀")
    st.markdown("Convert natural language queries into SQL queries effortlessly! 💡")

    # Input area for the natural language query
    user_query = st.text_area(
        "Enter your query here:",
        height=150,
        placeholder="E.g., 'Show me the top 10 customers by total purchase amount.' 🛒"
    )

    if st.button("Convert and Execute 🔄"):
        if not user_query.strip():
            st.warning("⚠️ Please enter a valid query.")
            return

        # Convert the natural language query to SQL using a spinner
        with st.spinner("🧠 Converting text to SQL query..."):
            try:
                sql_query = text_to_sql(user_query)
            except Exception as e:
                st.error(f"❌ Error during text-to-SQL conversion: {e}")
                return

        st.subheader("Generated SQL Query 📜")
        st.code(sql_query, language="sql")

        # Execute the generated SQL query on the database using a spinner
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
