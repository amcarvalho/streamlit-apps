from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
import streamlit as st
from typing import Dict
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import snowflake.connector
import toml
import logging
import inspect
import os

secrets_file_path = '../../.streamlit/secrets.toml'

def get_secrets() -> Dict[str, str]:
    """
    Returns a dictionary containing key value pairs representing how to connect to 
    a Snowflake database. Defaults to read those from a secrets.toml file stored in 
    this repo's .steamlit/secrets.toml folder.

    Should be used within your main streamlit `app.py` file. The return dictionary
    should be assigning to a variable called `secrets`.
    """
    with open(secrets_file_path) as f:
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

def _get_pkb(_secrets, account):
    p_key= serialization.load_pem_private_key(
        _secrets[account]['private_key'],
        password=_secrets[account]['passphrase'],
        backend=default_backend()
    )

    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return pkb

@st.cache_resource(show_spinner="Connecting to Snowflake...")
def get_connection(_secrets, authentication_method="user_session", api="snowpark", account="default_service_account"):
    """
    Establishes a connection to Snowflake based on the specified API and authentication method.

    This function retrieves connection parameters from the provided secrets based on the current 
    environment (local or production). It supports two APIs: Snowpark and the Snowflake connector. 
    Depending on the environment and authentication method, it either uses local development secrets 
    or retrieves the appropriate secrets for the specified service account used to connect to Snowflake.

    Parameters:
    ----------
    _secrets : dict
        A dictionary containing sensitive information required for connecting to Snowflake. 
        It should include keys for 'local_development' and production service accounts as specified.

    authentication_method : str, optional
        The method of authentication to use. Default is "user_session". 
        If set to "user_session", it retrieves an active session instead of using secrets.

    api : str, optional
        The API to use for the connection. Can be either "snowpark" or "connector". 
        Default is "snowpark".

    account : str, optional
        The account identifier to use when not in local development. 
        Default is "default_service_account".

    Returns:
    -------
    Session or Connection
        Returns a Snowpark Session if the API is "snowpark", or a Snowflake connector 
        connection if the API is "connector".

    Raises:
    ------
    KeyError
        If the specified account does not exist in the _secrets dictionary.

    Environment:
    ------------
    The function checks the environment variable 'STREAMLIT_ENV' to determine if it is 
    running in a local development environment or in production.

    Notes:
    -----
    - If running in a local environment, it always uses the 'local_development' secrets.
    - If the authentication method is "user_session", it bypasses the secrets and 
      retrieves the active session directly.
    """
    environment = os.getenv('STREAMLIT_ENV', 'local')
    if environment == "local":
        # If local development, always use local_development secrets
        parameters = {
            "account": _secrets['local_development']['account'],
            "user": _secrets['local_development']['user'],
            "password": _secrets['local_development']['password'],
            "client_session_keep_alive": _secrets['local_development'].get('client_session_keep_alive', True),
        }

        if api == "snowpark":
            return Session.builder.configs(parameters).create()
        elif api == "connector":
            return snowflake.connector.connect(**parameters)
    else:
        print("I GOT HERE")
        if authentication_method == "user_session":
            return get_active_session()
        else:
            pkb = _get_pkb(_secrets, account)

            parameters = {
                "account": _secrets[account]['account'],
                "user": _secrets[account]['user'],
                "private_key": pkb,
                "client_session_keep_alive": _secrets[account].get('client_session_keep_alive', True),
            }

            ctx = snowflake.connector.connect(
                **parameters
            )

            if api == "snowpark":
                return Session.builder.configs(parameters).create()
            elif api == "connector":
                return snowflake.connector.connect(**parameters)