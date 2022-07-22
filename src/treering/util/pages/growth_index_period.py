import streamlit as st
import os
import glob
import pandas as pd
import numpy as np
import altair as alt
from urllib.error import URLError


def get_current_dir():
    return os.getcwd()


def get_dataset_location():
    return os.path.join(get_current_dir(), "OpenData")


@st.cache
def get_data():
    directory = get_dataset_location()
    all_files = glob.glob(directory + "/*.csv")

    df = pd.DataFrame()

    for filename in all_files:
        if filename.endswith(".csv"):
            f = open(filename, 'r')
            csv_file = pd.read_csv(filename, index_col=None, header=0)
            df = pd.concat([df, csv_file], axis=0)
            f.close()

    df.rename(columns={'res.Lbai.normalized': 'growth_index'}, inplace=True)
    df.drop(["uid_tree", "uid_radius", "SummerSMI", "SummerSMI.t_1", "Ecoregions"], axis=1, inplace=True)
    df = df.groupby(['year'], as_index=False)['growth_index'].mean()
    # df = df.pivot(index='species', columns='year', values='growth_index')
    df = df.replace(np.nan, 0)
    df.columns = df.columns.astype(str)
    return df


def growth_index_period():
    st.markdown("---")

    st.markdown("## Summary of the Growth Index by Year")

    st.markdown("""
       ### Growth Index by year
       """)

    st.markdown("---")

    left_info_col, right_info_col = st.columns([1, 3])

    with left_info_col:
        try:
            df = get_data()
            st.write( df.sort_index())

        except URLError as e:
            st.error(
                """
                *This demo requires internet access.*
                Connection error: %s
            """
                % e.reason
            )

    with right_info_col:

        chart = (alt.Chart(df)
            .mark_area(opacity=0.3)
            .encode(
            x="year:N",
            y=alt.Y("growth_index:Q"))
        ).properties(
            height=500,
            width=100)

        st.altair_chart(chart, use_container_width=True)