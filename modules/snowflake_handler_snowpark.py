from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import pandas as pd
import streamlit as st

@st.cache_resource(show_spinner="Connecting to Snowflake...")
def get_connection(connection_name="snowflake"):
    try:
        return get_active_session()
    except:
        section = st.secrets[f"connections_{connection_name}"]
        parameters = {
            "account": section["account"],
            "user": section["user"],
            "password": section["password"],
            "client_session_keep_alive": section.get("client_session_keep_alive", True)
        }
        return Session.builder.configs(parameters).create()

@st.cache_data(ttl=3600, show_spinner="Running query...")
def run_query_into_df(_connection, query):
    try:
        rows = _connection.sql(query).collect()
        return pd.DataFrame(rows).convert_dtypes()
    except Exception as e:
        st.error(e);
        return None
