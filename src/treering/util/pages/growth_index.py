import streamlit as st
import pandas as pd
from urllib.error import URLError
import altair as alt
import os
import glob
import numpy as np
from ..scripts.data_pool import my_data


@st.cache()
def get_data():

    df = my_data().get_data()
    df.rename(columns={'res.Lbai.normalized': 'growth_index'}, inplace=True)
    df.drop(["uid_tree", "uid_radius", "SummerSMI", "SummerSMI.t_1", "Ecoregions"], axis=1, inplace=True)
    df = df.groupby(['species', 'year'], as_index=False)['growth_index'].mean()
    df = df.pivot(index='species', columns='year', values='growth_index')
    df = df.replace(np.nan, 0)
    df.columns = df.columns.astype(str)

    return df

def growth_index():

    st.markdown("---")

    st.markdown("#### Summary of the Tree Ring Analysis")

    st.markdown("""
    -NEED TO IMPLEMENT
    """)
    left_info_col, right_info_col = st.columns([3,1])

    with left_info_col:
        try:
            df = get_data()
            species = st.multiselect(
                "Choose species", list(df.index.unique()), ['PICEGLA', 'ABIEBAL']
            )
            if not species:
                st.error("Please select at least one specie.")
            else:
                data = df.loc[species]
                st.write("### Growth Index By Species", data.sort_index())

                data = data.T.reset_index()
                data = pd.melt(data, id_vars=["year"]).rename(columns={"index": "year", "value": "growth_index"})

                chart = (
                    alt.Chart(data)
                        .mark_area(opacity=0.3)
                        .encode(
                        x="year:T",
                        y=alt.Y("growth_index:Q", stack=None),
                        color="species:N",
                    )
                )
                st.altair_chart(chart, use_container_width=True)
        except URLError as e:
            st.error(
                """
                *This demo requires internet access.*
                Connection error: %s
            """
                % e.reason
            )

