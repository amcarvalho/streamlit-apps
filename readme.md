This repo allows creation and deployment of Snowflake Streamlit Native Apps.

# Local Development
In order to test your development locally, you will need to edit the file `secrets.toml` within the top-level folder `.streamlit`.

Edit the `local_development` sections of the file and change 3 variables:
```
[local_development]
account = "account_locator.region.cloud_provider" # Your Snowflake account
user = "first_name.last_name@domain.com" # Your Snowflake username
password = "my_password" # Your Snowflake password
client_session_keep_alive = true
```

Please not that although this repo provides a templated version of this file, that file has been added to `.ignore` and as such your changes won't be commited

# How to Create an App
Each new App should be created within a subfolder of the `apps` top-folder. Within each of these you should have at least 2 files:
* A `requirements.txt` file describing which python packages are required for your application
* An `app.py` file which will contain the main entrypoint to your streamlit application
* A `config.toml` describing some aspects of how the application will connect to Snowflake

This repo provides a set of common libraries which can be used by all applications. These libraries will be included in the packages of all applications that are deployed to Snowflake.