
import streamlit as st

import os


def get_current_dir():
    return os.getcwd()


def get_dataset_location():
    return os.path.join(get_current_dir(),"OpenData")

def manage_data_page():


    st.markdown("---")

    st.markdown("#### MANAGE DATA HERE")

    st.markdown("""
    Upload new dataset for evolution
    """)
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
     bytes_data = uploaded_file.read()

     with open(os.path.join(get_dataset_location(),uploaded_file.name), "wb") as file1:
         file1.write(uploaded_file.getbuffer())
         file1.close()
         st.write("filename:", uploaded_file.name, "Uploaded Successfully")


