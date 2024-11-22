use schema development_db.acarvalho;

put file:///Users/alexandrecarvalho/Documents/streamlit-apps/app.py @streamlit_apps
    overwrite=true auto_compress=false;
put file:///Users/alexandrecarvalho/Documents/streamlit-apps/requirements.txt @streamlit_apps
    overwrite=true auto_compress=false;
put file:///Users/alexandrecarvalho/Documents/streamlit-apps/modules/sf_handler_snowpark.py @streamlit_apps/modules
    overwrite=true auto_compress=false;

create or replace streamlit first_streamlit_app_acarvalho
    root_location = '@development_db.acarvalho.streamlit_apps'
    main_file = '/app.py'
    query_warehouse = 'COMPUTE_WH'
    title = 'Test Streamlit App (Alex)';

show streamlits;