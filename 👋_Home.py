import streamlit as st
import os
import signal
import importlib.util

# Function to load custom pages dynamically
# def load_custom_page(page_name):
    # file_path = os.path.join("custom_pages", f"{page_name}.py")
    # spec = importlib.util.spec_from_file_location(page_name, file_path)
    # module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module)

# # Get the list of custom pages
# custom_page_files = os.listdir('custom_pages')
# custom_pages = [os.path.splitext(file)[0] for file in custom_page_files if file.endswith('.py')]

# # Sidebar for custom page navigation
# st.sidebar.title("Navigation")
# custom_page = st.sidebar.selectbox("Select Custom Page", custom_pages)

# # Load the selected custom page
# load_custom_page(custom_page)