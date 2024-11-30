# Snowflake Streamlit Applications

This repository allows the creation and deployment of Snowflake Streamlit Applications.

## Initial Setup

Please follow these steps carefully for the initial setup:

1. Clone this repository by running:
    ```bash
    git clone https://github.com/amcarvalho/streamlit-apps && cd streamlit-apps
    ```

2. Create a Python virtual environment:
    ```bash
    python3 -m venv venv
    ```

3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a file called `secrets.toml` within the `.streamlit` folder in the root directory of the repository. You can use the example file `secrets.toml.example` as a reference.

    The `secrets.toml` file contains two sections:
    - `local_development`: Configure your Snowflake credentials for local development.
    - `deployment`: Configure Snowflake credentials if you need to deploy the applications to Snowflake locally. This is not recommended.

    You can request support from one of your team's developers if needed.

## Creating an Application

Create each new application within a subfolder of the `apps` top-level folder. Each application should contain at least two files:
- `app.py`: The main entry point for your Streamlit application.
- `app.conf`: Contains configuration options for the application, such as:
    - `app_name`: The name of the Streamlit application.
    - `allowed_roles`: Snowflake roles that will have access to the application.

This repository provides a set of common libraries that can be used by all applications. These libraries will be included in the packages of all applications deployed to Snowflake.

There are two example starter apps that you can use to understand how to develop a new application and leverage some of the most common methods provided by the libraries.

## Snowflake Connections

The most important method provided by the common libraries is the `get_connection` method in the `utils` package. This method makes it easy to retrieve a Snowflake connection and use it to run queries. The method works both in local development and in production.

- In local development mode, the connection uses your Snowflake credentials specified in the `secrets.toml` file, including which role will be used to run the queries.
- In production, the connection leverages Snowpark's `get_active_session` method. This means that the application will use the session the user created when they logged on to Snowflake.

## Deployment

This repository includes a GitHub workflow that will automatically redeploy all applications to Snowflake whenever a code change is pushed to the master branch.

When each application is deployed, a schema will be created for that application. The schema is not recreated on each deployment of the same application.

The roles specified to have access to the application will be granted write permissions to this schema. This schema will also contain a stage where the application codebase is uploaded, allowing the application to run in Snowflake's cloud.

## Accessing an Application

You can access an application in Snowflake's UI via the Projects -> Streamlit sidebar menu. Once you choose one of the applications, it will start immediately. You can copy the URL from your browser and share it with users you want to provide access to.

---

If you need any further assistance, feel free to reach out to your team's developers or consult the example starter apps for more guidance.
