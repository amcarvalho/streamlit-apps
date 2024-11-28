import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import modules.utils as utils
import streamlit as st
logger = utils.configure_logging_and_get_logger()
secrets = utils.get_secrets()
session = utils.get_connection(
    secrets,
    api="snowpark"
)
logger.info("Connection Established")

def get_databases():
    databases = session.sql("SHOW DATABASES").collect()
    return [db['name'] for db in databases]

def get_schemas(database):
    schemas = session.sql(f"SHOW SCHEMAS IN DATABASE {database}").collect()
    return [schema['name'] for schema in schemas]

def get_tables(database, schema):
    tables = session.sql(f"SHOW TABLES IN SCHEMA {database}.{schema}").collect()
    return [table['name'] for table in tables]

def get_table_data(session, database, schema, table):
    data = session.table(f"{database}.{schema}.{table}").limit(10).collect() 
    return data

logger.info('Application Started')
st.title("Sample Application")
st.sidebar.title("Snowflake Browser")
databases = get_databases()
selected_database = st.sidebar.selectbox("Select Database", databases)

if selected_database:
    schemas = get_schemas(selected_database)
    selected_schema = st.sidebar.selectbox("Select Schema", schemas)

    if selected_schema:
        tables = get_tables(selected_database, selected_schema)
        selected_table = st.sidebar.selectbox("Select Table", tables)

        if selected_table:
            table_data = get_table_data(session, selected_database, selected_schema, selected_table)
            st.table(table_data)
        else:
            st.write("No tables found in the selected schema.")
