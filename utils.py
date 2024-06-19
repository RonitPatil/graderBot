import os
import streamlit as st
import shutil

def get_files_in_directory(directory):
    """
    This function helps us to get the file path along with filename.
    """
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

def save_uploaded_file(uploaded_files):
    """
    Function to save uploaded file.
    """
    remove_existing_files('data')
    for uploaded_file in uploaded_files:
        file_path = os.path.join('data', uploaded_file.name)
        with open(file_path, "wb") as file:
            file.write(uploaded_file.read())
    st.success("File uploaded successfully")

def remove_existing_files(files):
    for file_path in files:
        file_path = os.path.normpath(file_path)  # Normalize the file path
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                st.write(f"Removed file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                st.write(f"Removed directory: {file_path}")
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")