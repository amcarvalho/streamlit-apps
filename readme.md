This repo allows creation and deployment of Snowflake Streamlit Native Apps.

# Initial Setup
The initial setup involves several steps. Please read and follow these steps carefully.

* Fork/copy this repo into your own organisation or project. If this repo already is a copy
within your organisation, you will only need to clone this repo. 

* Create a python virtual environment. 

* Create a file called `secrets.toml` within a folder called `.streamlit` within the root of
this repo. This file will contain secrets used to connect to Snowflake using your own account.
More details about what this file should contain are explained in the 
[Configure secrets.toml file](#configure-secrets.toml-file) section.

## Configure secrets.toml file
Create a file called `secrets.toml` within the top-level folder `.streamlit`.

Copy/paste the snippet below into that file. Change the values to the details of your Snowflake
account.
```
[local_development]
account = "account_locator.region.cloud_provider" # Your Snowflake account
user = "first_name.last_name@domain.com" # Your Snowflake username
password = "my_password" # Your Snowflake password
client_session_keep_alive = true
```

Do not commit this file to the repo. The `.streamlit` folder has already been added to `.gitignore`,
so unless you explicitly remove it from there, you won't accidentally commit your credentials into
the repo/github.

# How to Create an App
Create each new App within a subfolder of the `apps` top-folder. Within each of these you should have at least 2 files:
- An `app.py` file which will contain the main entrypoint to your streamlit application
- A `app.conf` describing some configuration options for each app, namely:
    - app_name: The name of the streamlit Application
    - allowed_roles: which Snowflake roles will have access to the app

This repo provides a set of common libraries which can be used by all applications. These libraries will be included in the packages of all applications that are deployed to Snowflake.

# Deployment
Whenever each app is deployed, a schema will be created for that app. The roles which are specified
to have access to the app will be grant write permissions to this schema. This schema will also 
contain a stage where the app codebase is uploaded into in order to run in Snowflake's cloud.