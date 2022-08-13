import streamlit
import streamlit as st
from PIL import Image
import os
import numpy as np
from ..scripts.data_pool import my_data

directory = os.getcwd()

total_trees = 0
min_year = 0
max_year = 0
total_sites = 0
total_projects = 0
total_species = 0
total_instances = 0

def get_current_dir():
    return os.getcwd()


def get_image_location():
    return os.path.join(get_current_dir(),"images")


@st.cache()
def get_data():

    df = my_data().get_data()
    df.rename(columns={'res.Lbai.normalized': 'growth_index'}, inplace=True)
    df.drop(["uid_radius", "SummerSMI", "SummerSMI.t_1", "Ecoregions"], axis=1, inplace=True)

    global total_trees
    total_trees = df['uid_tree'].nunique()

    global min_year
    min_year = df['year'].min()

    global max_year
    max_year = df['year'].max()

    global total_sites
    total_sites = df['uid_site'].nunique()

    global total_projects
    total_projects = df['uid_project'].nunique()

    global total_instances
    total_instances = df.shape[0]

    global total_species
    total_species = df['species'].nunique()

    # df = df.groupby(['species', 'year'], as_index=False)['growth_index'].mean()
    # df = df.pivot(index='species', columns='year', values='growth_index')
    # df = df.replace(np.nan, 0)
    # df.columns = df.columns.astype(str)


def overview_page():
    get_data()
    #im = Image.open(os.path.join(get_image_location(),"tree_ring_img.jpg"))
    im2 = Image.open(os.path.join(get_image_location(),"Picture1.png"))
    #im3 = Image.open(os.path.join(get_image_location(),"Picture2.png"))


    st.markdown("#### Summary of the Tree Ring Analysis")

    st.markdown("""
    The tree ring analysis database is a collection of 1,633,826 instances spanning over 67 years containing 47 projects and samples from 66
    species of trees
    """)

    "====================================METRICS ROW 1==============================================================="
    st.markdown("---")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    #col1.metric(label="Total Tress", value=total_trees, delta="1.2 °F")
    col1.metric(label="Total Trees", value= "{:,}".format(total_trees))

    total_year = f'{min_year} to {max_year}'
    col2.metric(label="Total Years", value= total_year)

    col3.metric(label="Total Sites", value= "{:,}".format(total_sites))

    col4.metric(label="Total Contributors/Projects", value= total_projects)

    col5.metric(label='Total Instances', value= "{:,}".format(total_instances))

    col6.metric(label='Total Species', value=total_species)

    "====================================METRICS ROW 2==============================================================="
    st.image(im2, caption='')

    # left_col.image(im2, caption='')
    # left_col.markdown("""## 4471""")
    # left_col.markdown(" sites where observed and recorded for the data")
    #
    # ## Right Side
    # right_col.markdown("""## 66 """)
    # right_col.markdown("species where analysed for their growth patterns")