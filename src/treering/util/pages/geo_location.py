import streamlit as st
from urllib.error import URLError
import numpy as np
import pydeck as pdk
import pandas as pd
import math
from geopy.geocoders import Nominatim
from ..scripts.data_pool import my_data


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
    df = df.groupby(['latitude', 'longitude'], as_index=False)['growth_index'].mean()

    cols = ['longitude','latitude']
    # Create new column coordinates
    df['coordinates'] = df[cols].apply(lambda row: list(row.values), axis=1)
    #df['address'] = df['coordinates'].apply(lambda coord: get_location_names(coord))

    df["growth_index_radius"] = df["growth_index"].apply(lambda growth_index_count: math.exp(growth_index_count))

    df = df.replace(np.nan, 0)
    df.columns = df.columns.astype(str)
    return df



def geo_location():
    st.markdown("---")

    st.markdown("#### Summary of the Tree Ring Analysis")

    st.markdown("""
     The tree ring analysis database is a collection of 1,633,826 instances spanning over 67 years containing 47 projects and samples from 66
    species of trees
    """)

    left_info_col, right_info_col = st.columns([1, 3])

    with left_info_col:

        try:
            df = get_data()
            st.dataframe(df)

        except URLError as e:
            st.error(
                """
                *This demo requires internet access.*
                Connection error: %s
            """
                % e.reason
            )


    with right_info_col:
        try:
            df = get_data()
            # SCATTERPLOT_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json"
            # df = pd.read_json(SCATTERPLOT_LAYER_DATA)

            # Use pandas to calculate additional data
            # df["exits_radius"] = df["exits"].apply(lambda exits_count: math.sqrt(exits_count))

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
                ], tooltip={"text": "{name}\n{address}"}))

        except URLError as e:
            st.error(
                """
                *This demo requires internet access.*
                Connection error: %s
            """
                % e.reason
            )