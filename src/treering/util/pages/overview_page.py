import streamlit as st
from PIL import Image
import os


directory = os.getcwd()


def get_current_dir():
    return os.getcwd()


def get_image_location():
    return os.path.join(get_current_dir(),"images")


def overview_page():

    im = Image.open(os.path.join(get_image_location(),"tree_ring_img.jpg"))
    im2 = Image.open(os.path.join(get_image_location(),"Picture1.png"))
    im3 = Image.open(os.path.join(get_image_location(),"Picture2.png"))

    left_col, right_col = st.columns(2)
    right_col.image(im, caption='')

    st.markdown("---")

    left_col.markdown("#### Summary of the Tree Ring Analysis")

    left_col.markdown("""
    The tree ring analysis database is a collection of 1,633,826 instances spanning over 67 years containing 47 projects and samples from 66
    species of trees
    """)
    left_col.image(im2, caption='')
    left_col.markdown("""## 4471""")
    left_col.markdown(" sites where observed and recorded for the data")
    right_col.image(im3, caption='')
    right_col.markdown("""## 66 """)
    right_col.markdown("species where analysed for their growth patterns")