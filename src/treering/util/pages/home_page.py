import streamlit as st
import webbrowser

import os
from PIL import Image

directory = os.getcwd()

def get_current_dir():
    return os.getcwd()


def get_image_location():
    return os.path.join(get_current_dir(),"images")
def home_page():

    im = Image.open(os.path.join(get_image_location(),"cover.jpg"))


    left_col, right_col = st.columns(2)
    left_col.image(im, caption='')
    right_col.markdown("# TREE RING ANALYSIS")
    right_col.markdown("### A tool for analyzing tree growth in canada")

    st.sidebar.markdown("## Reference Links")
    url_Pandas = 'https://pandas.pydata.org'
    url_Numpy = 'https://numpy.org/doc/stable/'
    url_Matplotlib = 'https://matplotlib.org'

    if st.sidebar.button('Pandas'):
        webbrowser.open_new_tab(url_Pandas)

    if st.sidebar.button('Numpy'):
        webbrowser.open_new_tab(url_Numpy)

    if st.sidebar.button('Matplotlib'):
        webbrowser.open_new_tab(url_Matplotlib)

    st.markdown("---")

    st.markdown(
        """
        ### Summary
       
        """
    )

    left_col, right_col = st.columns(2)

    left_col.markdown(
        """
        ### Usage

        To the left, is a dropdown main menu for navigating to 
        each page in the TREE RING ANALYSIS:

        - **Home Page:** We are here!
        

        """
    )
    st.markdown("---")

    left_info_col, right_info_col = st.columns(2)

    left_info_col.markdown(
        f"""
        ### Team Members 
        ### Sandeep Kolapineni
        ### Samir Mendoza
        ### Tom James
        
        
        Please feel free to contact us with any issues, comments, or questions.

       
        """,
        unsafe_allow_html=True,
    )

    right_info_col.markdown(
        """
        ### DATA

       
         """
    )

    right_info_col.markdown(
        """
        ### DATA 
       
        """

    )
