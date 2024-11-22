import os
import snowflake.connector
import streamlit as st

def get_connection(connection_name="snowflake"):
    """
    Establishes a connection to Snowflake using credentials from Streamlit secrets.
    """
    section = st.secrets[f"connections_{connection_name}"]
    return snowflake.connector.connect(
        account=section["account"],
        user=section["user"],
        password=section["password"],
        client_session_keep_alive=section.get("client_session_keep_alive", False),
    )

@st.cache_data(ttl=3600, show_spinner="Running query...")
def run_query(_conn, query, result_format):
    """
    Executes a query on the provided Snowflake connection.
    
    Args:
        _conn: Snowflake connection object.
        query: SQL query to execute.
        result_format: Format of the result ('df' for pandas DataFrame).
        
    Returns:
        Query result in the requested format.
    """
    with _conn.cursor() as cur:
        cur.execute(query)
        if result_format == 'df':
            return cur.fetch_pandas_all()
        return cur.fetchall()
