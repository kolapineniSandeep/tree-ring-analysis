import streamlit as st
from urllib.error import URLError
import numpy as np
import pydeck as pdk
import pandas as pd
import math
from geopy.geocoders import Nominatim
from ..scripts.data_pool import my_data
import plotly.express as px
from PIL import Image
import os

directory = os.getcwd()

@st.cache
def get_location_names(coordinates):
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.reverse(coordinates)
    return location.address

@st.cache
def get_data():

    df = my_data().get_data()
    df.rename(columns={'res.Lbai.normalized': 'growth_index'}, inplace=True)
    df.drop(["uid_tree", "uid_radius", "SummerSMI", "SummerSMI.t_1", "Ecoregions"], axis=1, inplace=True)
    df = df.groupby(['latitude', 'longitude','species', 'uid_site'], as_index=False)['growth_index'].mean()

    cols = ['longitude','latitude']
    # Create new column coordinates
    df['coordinates'] = df[cols].apply(lambda row: list(row.values), axis=1)
    #df['address'] = df['coordinates'].apply(lambda coord: get_location_names(coord))

    df["growth_index_radius"] = df["growth_index"].apply(lambda growth_index_count: math.exp(growth_index_count))

    df = df.replace(np.nan, 0)
    df.columns = df.columns.astype(str)
    return df

@st.cache()
def get_data_province():
    df_province = my_data().get_data_with_province()

    return df_province

def get_current_dir():
    return os.getcwd()


def get_image_location():
    return os.path.join(get_current_dir(),"images")



def geo_location():

    st.markdown("---")

    st.markdown("#### Summary of the Tree Ring Analysis")

    st.markdown("""
    Trees by Location
    """)


    try:
        df = get_data()

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v10',
            initial_view_state=pdk.ViewState(
                latitude=49.859504489017894,
                longitude=-97.11985287235485,
                zoom= 3,
                bearing=0,
                pitch=0
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    pickable=True,
                    opacity=0.8,
                    stroked=True,
                    filled=True,
                    radius_scale=6,
                    radius_min_pixels=1,
                    radius_max_pixels=100,
                    line_width_min_pixels=1,
                    get_position="coordinates",
                    get_radius="growth_index_radius",
                    get_fill_color=[0, 255, 128],
                    get_line_color=[0, 0, 0],
                ),
            ], tooltip={"text": "{species}\n{uid_site}"}))

    except URLError as e:
        st.error(
            """
            *This demo requires internet access.*
            Connection error: %s
        """
            % e.reason
        )

    st.markdown('-----------------------------')
    ''' =======================================PROVINCE TABLE========================================================'''

    df_prov = get_data_province()

    # creating a group by State, Total trees, Avg Growth Index
    df_group_province = df_prov.groupby("state").agg(
        {"uid_tree": ["nunique"],
         "uid_site": ["nunique"],
         "species": ["nunique"],
         "year": ["min", "max"],
         "growth_index": ["mean", "min", "max"]}
    ).reset_index()

    # Fixing Columns name
    df_group_province.columns = df_group_province.columns.map('_'.join)

    # Rename Columns Names
    df_group_province = df_group_province.rename(
        columns={
            "state_": "Province/Region",
            "uid_tree_nunique": "Total trees",
            "uid_site_nunique": "Total Sites",
            "species_nunique": "Total Species",
            "year_min": "Data From",
            "year_max": "Data To",
            "growth_index_min": "Min G.I.",
            "growth_index_max": "Max G.I.",
            "growth_index_mean": "Avg G.I."
        })

    # Creating a new column % Total Tree
    df_group_province['% Total Tree'] = (df_group_province.groupby('Province/Region')['Total trees'].transform('mean') /
                                         df_group_province['Total trees'].sum())

    # Apply % format
    df_group_province['% Total Tree'] = df_group_province['% Total Tree'].apply(lambda x: "{0:.2f}%".format(x * 100))

    # Concatenating year columns
    df_group_province['Year Range'] = df_group_province['Data From'].astype(str) + '-' + df_group_province[
        'Data To'].astype(str)

    # Removin Data From and Data To columns
    df_group_province = df_group_province.drop(['Data From', 'Data To'], axis=1)

    # Reorder columns
    df_group_province = df_group_province[['Province/Region',
                                           'Total trees',
                                           '% Total Tree',
                                           'Total Sites',
                                           'Total Species',
                                           'Year Range',
                                           'Min G.I.',
                                           'Max G.I.',
                                           'Avg G.I.']]

    df_group_province['Avg G.I.'] = df_group_province['Avg G.I.'].round(decimals=4)

    # df_group_province
    df_group_province.style.bar(subset=['Total trees'], align='left', color=['#d65f5f', '#5fba7d'])

    fig_3 = px.bar(df_group_province, x="Avg G.I.", y="Province/Region", orientation='h',
                   hover_data=["Max G.I.", "Min G.I.", "Year Range"],
                   height=650, color='Province/Region')

    st.write("### Bar chart of Growth Index By Province/Region")
    st.plotly_chart(fig_3, use_container_width=True)

    st.markdown('---------')

    st.write("### Stadistic Table about the Growth Index By Province/Region")
    st.table(data=df_group_province)
