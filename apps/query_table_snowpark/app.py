import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import pandas as pd
import modules.snowflake_handler_snowpark as sh
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logging.getLogger("snowflake.connector").setLevel(logging.WARNING)
connection = sh.get_connection()
logging.info("Connection established.")

def process_input(user_input):
    df = sh.run_query_into_df(connection, f"select * from {user_input}")
    return df

# Title of the app
st.title("Data Fetcher")

st.sidebar.header("Input Section")
user_input = st.sidebar.text_input("Enter a value:")
submit_button = st.sidebar.button("Submit")

if submit_button:
    if user_input:
        try:
            df = process_input(user_input)
            if not df.empty:
                st.table(df)
            else:
                st.info("The query returned no data.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a value in the text field.")