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
    url_seaborn='https://seaborn.pydata.org/'
    url_git='https://github.com/kolapineniSandeep/tree-ring-analysis'
    col1,col2=st.sidebar.columns(2)
    if col1.button('Pandas Libreary'):
        webbrowser.open_new_tab(url_Pandas)

    if col1.button('Numpy'):
        webbrowser.open_new_tab(url_Numpy)
    if col1.button('GITHUB'):
        webbrowser.open_new_tab(url_git)
    if col2.button('Matplotlib'):
        webbrowser.open_new_tab(url_Matplotlib)
    if col2.button('seaborn graphs'):
        webbrowser.open_new_tab(url_seaborn)
    st.markdown("---")




    st.markdown(
        """
        ### Usage

        To the left, is a dropdown main menu for navigating to 
        each page in the TREE RING ANALYSIS:

        - **Home Page:** We are here!
        - **Overview Page:** Provide all insights about data, like number of trees, and group by spices and sites and many more.
        - **Outlier Page:** In this page we can compare outliers among spices over the years, using table and box plot
        - **Growth Index By Spices Page:** find growth index of each spices over the years 
        - **Growth Index By Geo Location:** Points the trees in map based on geolocation
        - **Manage dataset :** We can upload and manage new datasets here!


        """
    )
    st.markdown("---")

    left_info_col, right_info_col = st.columns(2)

    left_info_col.markdown(
        f"""
        ### Team Members 
        ### Sandeep Kolapineni
        ### Samir Abisai Mendoza Lozano
        ### Tom James Madolil
        
        
        Please feel free to contact us with any issues, comments, or questions.
       - **Left side of the application menu, you can find git hub link.**
        Please drop feedbacks, suggestions. 
        ### we are welcoming contributors 

       
        """,
        unsafe_allow_html=True,
    )

    with right_info_col:
        im = Image.open(os.path.join(get_image_location(),"tree_ring_img.jpg"))
        st.image(im, width=360)

    right_info_col.markdown(
        """
        
        The aim of this project is to understand tree growth index in canadian forest and also calculate productivity
       of forest growth in canada. We incorporated with canada forest services and took dataset. The data repository that currently contains
       tree-ring measurements from 40 206 tree samples from 4594 sites and 62 tree species from all Canadian provinces and territories
        The out come of the project is to create interactive dash board which provide lot of insights, and identify
        the trees, spices and ares which are at at greatest risk of forest losses. 
        """

    )
