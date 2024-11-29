import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import modules.utils as utils
import streamlit as st

logger = utils.configure_logging_and_get_logger()
session = utils.get_connection(api="snowpark")
logger.info("Connection Established")

def create_table_from_csv(database, schema, table_name, csv_file):
    try:
        df = pd.read_csv(csv_file)
        column_definitions = ", ".join([f"{col} STRING" for col in df.columns])
        create_table_statement = f"CREATE OR REPLACE TABLE {database}.{schema}.{table_name} ({column_definitions})"
        session.sql(create_table_statement).collect()
        logger.info(f"Table {database}.{schema}.{table_name} created with columns: {column_definitions}")

        session.write_pandas(df, f"{database}.{schema}.{table_name}", overwrite=True)
        logger.info(f"Data from {csv_file.name} uploaded to {database}.{schema}.{table_name}")
        st.success(f"Data uploaded to {database}.{schema}.{table_name}")
    except Exception as e:
        logger.error(f"Error creating table or uploading CSV file: {e}")
        st.error(f"Error creating table or uploading CSV file: {e}")

logger.info('Application Started')
st.title("CSV Uploader to Snowflake")
st.sidebar.title("Table Creation")

database = st.sidebar.text_input("Enter Database Name")
schema = st.sidebar.text_input("Enter Schema Name")
table_name = st.sidebar.text_input("Enter Table Name")

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if st.sidebar.button("Upload and Create Table") and uploaded_file and database and schema and table_name:
    create_table_from_csv(database, schema, table_name, uploaded_file)
else:
    st.sidebar.write("Please fill in all fields and upload a CSV file.")
