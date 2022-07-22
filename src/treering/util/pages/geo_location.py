import streamlit as st
from urllib.error import URLError

import pydeck as pdk
import pandas as pd
import math

def geo_location():
    st.markdown("---")

    st.markdown("#### Summary of the Tree Ring Analysis")

    st.markdown("""
    -NEED TO IMPLEMENT
    """)

    left_info_col, right_info_col = st.columns([4, 1])

    with left_info_col:
        try:

            SCATTERPLOT_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json"
            df = pd.read_json(SCATTERPLOT_LAYER_DATA)

            # Use pandas to calculate additional data
            df["exits_radius"] = df["exits"].apply(lambda exits_count: math.sqrt(exits_count))

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v10',
                initial_view_state=pdk.ViewState(
                    latitude=37.7749295,
                    longitude=-122.4194155,
                    zoom=10,
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
                        get_radius="exits_radius",
                        get_fill_color=[0, 255,128],
                        get_line_color=[0, 0, 0],
                    ),
                ],tooltip={"text": "{name}\n{address}"}))

        except URLError as e:
            st.error(
                """
                *This demo requires internet access.*
                Connection error: %s
            """
                % e.reason
            )
