import streamlit as st
import pandas as pd

# Title of the app
st.title("CSV File Uploader")

# Sidebar for file upload
st.sidebar.header("Upload CSV file")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write(df)
else:
    st.write("Please upload a CSV file.")

