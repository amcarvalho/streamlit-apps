import os
import toml
import utils

apps_folder = 'apps'
logger = utils.configure_logging_and_get_logger()
connection = utils.get_connection(
    api="connector", 
    account="deployment"
)
cursor = connection.cursor()


def get_deployment_config():
    with open('.streamlit/deploy.conf') as f:
        conf = toml.load(f)
    return conf


def get_apps(apps_folder):
    try:
        # Get the list of all entries in the given directory
        entries = os.listdir(apps_folder)
        
        # Filter out only the directories
        top_level_folders = [entry for entry in entries if os.path.isdir(os.path.join(apps_folder, entry))]
        
        return top_level_folders
    except FileNotFoundError:
        print("The specified folder was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_app_config(app):
    try:
        with open(f"{apps_folder}/{app}/app.conf") as f:
            conf = toml.load(f)
    except FileNotFoundError:
        return dict()
    return conf


def get_allowed_roles(app):
    conf = get_app_config(app)
    try:
        return conf['allowed_roles']
    except KeyError:
        return list()


def get_app_name(app):
    conf = get_app_config(app)
    try:
        return conf['name']
    except KeyError:
        return app


def get_app_warehouse(app):
    conf = get_app_config(app)
    try:
        return conf['warehouse']
    except KeyError:
        deployment_config = get_deployment_config()
        return deployment_config['warehouse']


def create_app_schema(app):
    deployment_config = get_deployment_config()
    database = deployment_config['database']
    schema = f"{database}.{app}"
    statement = f"create schema if not exists {schema}"
    logger.info(statement)
    cursor.execute(statement)
    for role in get_allowed_roles(app):
        statement = f"GRANT USAGE ON DATABASE {database} TO ROLE {role}"
        logger.info(statement)
        cursor.execute(statement)
        privileges = ['USAGE ON', 'CREATE TABLE ON', 'CREATE VIEW ON', 
                      'SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN', 'SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN',
                      'SELECT ON ALL VIEWS IN', 'SELECT ON FUTURE VIEWS IN']
        for privilege in privileges:
            statement = f"GRANT {privilege} SCHEMA {schema} TO ROLE {role}"
            logger.info(statement)
            cursor.execute(statement)


def _list_files_recursively(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def put_files_into_stage(app):
    current_folder = os.getcwd()
    deployment_config = get_deployment_config()
    database = deployment_config['database']
    stage = f"{database}.{app}.stage"
    logger.info(f"REMOVE @{stage}")
    cursor.execute(f"REMOVE @{stage}")
    logger.info(f"put file://{current_folder}/modules/utils.py @{stage}/modules auto_compress=false")
    cursor.execute(f"put file://{current_folder}/modules/utils.py @{stage}/modules auto_compress=false")
    files = _list_files_recursively(f"{current_folder}/apps/{app}")
    for file in files:
        filename = os.path.basename(file)
        remote_path = file.replace(f"{current_folder}/apps/{app}/", "")
        remote_path = remote_path.replace(filename, "")
        logger.info(f"put file://{file} @{stage}/{remote_path} auto_compress=false")
        cursor.execute(f"put file://{file} @{stage}/{remote_path} auto_compress=false")
    

def create_stage(app):
    deployment_config = get_deployment_config()
    database = deployment_config['database']
    stage = f"{database}.{app}.stage"
    logger.info(f"create stage if not exists {stage}")
    cursor.execute(f"create stage if not exists {stage}")


def create_streamlit(app):
    deployment_config = get_deployment_config()
    database = deployment_config['database']
    schema = f"{database}.{app}"
    statement = f"""
        create or replace streamlit {schema}.{app}
        root_location='@data_streamlit_apps.{app}.stage' 
        main_file='app.py' 
        query_warehouse='{get_app_warehouse(app)}'
        title = '{get_app_name(app)}';
        """
    logger.info(statement)
    cursor.execute(statement)
    for role in get_allowed_roles(app):
        logger.info(f"grant usage on streamlit {schema}.{app} to role {role}")
        cursor.execute(f"grant usage on streamlit {schema}.{app} to role {role}")


def create_app(app):
    create_app_schema(app)
    create_stage(app)
    put_files_into_stage(app)
    create_streamlit(app)
        

if __name__ == "__main__":
    apps = get_apps(apps_folder)

    try:
        for app in apps:
            logger.info(f"Creating App: {app}")
            create_app(app)
    finally:
        cursor.close()
        connection.close()
