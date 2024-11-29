import streamlit as st
from typing import Dict
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSessionException
from snowflake.snowpark import Session
import snowflake.connector
import toml
import logging
import inspect
import os

def _get_existing_file(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def get_secrets() -> Dict[str, str]:
    """
    Returns a dictionary containing key value pairs representing how to connect to 
    a Snowflake database. Defaults to read those from a secrets.toml file stored in 
    this repo's .streamlit/secrets.toml folder.

    Should be used within your main streamlit `app.py` file. The return dictionary
    should be assigned to a variable called `secrets`.
    """
    file_paths = [
        '../../.streamlit/secrets.toml',
        '../.streamlit/secrets.toml',
        '.streamlit/secrets.toml',
        'secrets.toml'
    ]
    secrets_path = _get_existing_file(file_paths)

    with open(secrets_path) as f:
        secrets = toml.load(f)
    return secrets


def _get_calling_script_folder():
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame, 2)
    calling_script_path = caller_frame[2].filename
    calling_script_dir = os.path.dirname(os.path.abspath(calling_script_path))
    folder_name = os.path.basename(calling_script_dir)
    return folder_name

def configure_logging_and_get_logger() -> logging.Logger:
    """
    Configures default logging settings for the application and returns a logger object.

    This function performs the following steps:
    1. Determines the name of the calling script's folder using a helper function 
    `_get_calling_script_folder()`. This will be the name of the streamlit application.
    2. Sets up the basic logging configuration with a logging level of DEBUG and a specified format.
    3. Configures the logging level for the "snowflake.connector" logger to WARNING.
    4. Creates and returns a logger object with the name of the calling script's folder.

    Returns:
    logging.Logger: A configured logger object for the calling script's folder.

    Example:
    >>> logger = configure_logging_and_get_logger()
    >>> logger.debug("This is a debug message")
    >>> logger.info("This is an info message")
    """
    name = _get_calling_script_folder()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        handlers=[logging.StreamHandler()]
    )
    logging.getLogger("snowflake.connector").setLevel(logging.WARNING)

    # Create a logger
    logger = logging.getLogger(name)
    return logger


@st.cache_resource(show_spinner="Connecting to Snowflake...")
def get_connection(api="snowpark", account="local_development"):
    try:
        # Production
        return get_active_session()
    except SnowparkSessionException:
        # Local Development
        secrets = get_secrets()
        parameters = {
            "account": secrets[account]['account'],
            "user": secrets[account]['user'],
            "password": secrets[account]['password'],
            "role": secrets[account]['role'],
            "warehouse": secrets[account]['warehouse'],
            "client_session_keep_alive": secrets[account].get('client_session_keep_alive', True),
        }

        if api == "snowpark":
            return Session.builder.configs(parameters).create()
        elif api == "connector":
            return snowflake.connector.connect(**parameters)