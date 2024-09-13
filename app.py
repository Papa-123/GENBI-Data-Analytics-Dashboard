import os
import streamlit as st
from langchain import SQLDatabase
from langchain_anthropic import ChatAnthropic
from langchain_experimental.sql import SQLDatabaseChain
import re

def extract_sql(query):
    """
    Extracts the SQL query from the response. It looks for the first occurrence of "SELECT"
    and ensures it ends with a proper SQL terminating character like ";" or the end of the string.
    """
    # First, try to match a complete SQL statement ending with a semicolon
    sql_match = re.search(r"SELECT\s.+?;\s*(?=(\n|$))", query, re.DOTALL | re.IGNORECASE)
    if sql_match:
        return sql_match.group(0).strip()
    
    # If no semicolon is found, try to match a SQL statement that ends with the end of the string
    sql_match = re.search(r"SELECT\s.+?(?=(\n|$))", query, re.DOTALL | re.IGNORECASE)
    if sql_match:
        return sql_match.group(0).strip()
    
    return None

def main():
    # Set your API key for Anthropic or another API
    os.environ['ANTHROPIC_API_KEY'] = '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'  # Replace with your API key

    # Streamlit app title
    st.title("Natural Language to SQL Query Generator")

    # Instructions
    st.write("Enter a natural language query to generate an SQL query:")

    # User input for the natural language query
    prompt = st.text_input("Enter your query:", value="")

    # Load your SQLite database file
    db_path = "D:/GENBI_project/dada.db"  # Replace with the path to your .db file
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    # Initialize the LLM (using Anthropic)
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        temperature=0,
        max_tokens=1024,
        timeout=None,
        max_retries=2
    )

    # Initialize the SQLDatabaseChain with the LLM and the database
    db_agent = SQLDatabaseChain(llm=llm, database=db, verbose=True)

    if prompt:
        try:
            # Generate the SQL query
            raw_query = db_agent.run(prompt)
            
            # Extract the SQL query from the response
            sql_query = extract_sql(raw_query)
            
            if sql_query:
                # Display the SQL query
                st.write("Generated SQL Query:")
                st.code(sql_query, language='sql')
            else:
                st.error("Could not extract a valid SQL query from the generated text.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
