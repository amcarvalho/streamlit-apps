This repo allows creation and deployment of Snowflake Streamlit Native Apps.

# Initial Setup
The initial setup involves several steps. Please read and follow these steps carefully.

* Fork/copy this repo into your own organisation or project. If this repo already is a copy
within your organisation, you will only need to clone this repo. 

* Create a file called `secrets.toml` within a folder called `.streamlit` within the root of
this repo. This file will contain secrets used to connect to Snowflake using your own account.
More details about what this file should contain are explained in the 
[Configure secrets.toml file](#configure-secrets.toml-file) section.

* Configure an environment variable named `STREAMLIT_ENV` to the value `local`. Follow 
[this guide](https://chlee.co/how-to-setup-environment-variables-for-windows-mac-and-linux/) 
if you don't know how to set environment variables on Windows/MacOS.

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
Each new App should be created within a subfolder of the `apps` top-folder. Within each of these you should have at least 2 files:
* A `requirements.txt` file describing which python packages are required for your application
* An `app.py` file which will contain the main entrypoint to your streamlit application
* A `config.toml` describing some aspects of how the application will connect to Snowflake

This repo provides a set of common libraries which can be used by all applications. These libraries will be included in the packages of all applications that are deployed to Snowflake.