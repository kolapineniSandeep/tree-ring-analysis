import streamlit as st
import pandas as pd
from urllib.error import URLError
import altair as alt
import plotly.express as px
import os
import glob
import numpy as np
from ..scripts.data_pool import my_data


@st.cache()
def get_data():

    df = my_data().get_data()
    df.rename(columns={'res.Lbai.normalized': 'growth_index'}, inplace=True)
    df.drop(["uid_tree", "uid_radius", "SummerSMI", "SummerSMI.t_1", "Ecoregions"], axis=1, inplace=True)

    return df


def growth_index():

    st.markdown("---")

    st.write("#### Summary of the Tree Ring Analysis")

    st.markdown("""
     Here you can filter and compare the growth index between different species, amoung of theese species are: 
     Picea glauca (42.0%), Picea mariana (17.5%), Picea abies (13.0%), Pinus strobus (10.2%), Picea rubens (8.0%), 
     Abies balsamea (1.1%), Picea x lutzii (1.1%), Acer saccharum (1.0%), 87 other species (6.0%)
    """)

    st.markdown('----------------------')

    try:
        df = get_data()
        df = df[df['year'] < 2017]
        df = df.groupby(['species', 'year'], as_index=False)['growth_index'].mean()
        df = df.pivot(index='species', columns='year', values='growth_index')
        df = df.replace(np.nan, 0)
        df.columns = df.columns.astype(str)


        species = st.multiselect(
            "Choose species", list(df.index.unique()), ['PICEGLA', 'ABIEBAL', 'ABIEAMA','PICEMAR','PINUSTR','PICERUB','ACERSAC']
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

    st.markdown('--------------')


    try:
        df = get_data()
        df = df[df['year'] < 2017]
        df = df.groupby(['year'], as_index=False)['growth_index'].mean()
        df = df.replace(np.nan, 0)
        df.columns = df.columns.astype(str)
        df['growth_index'] = df['growth_index'].round(decimals=4)

        fig = px.bar(df, y='growth_index', x='year', text='growth_index' ,text_auto='.004')
        fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)


        st.write("### Growth Index By years")
        st.plotly_chart(fig, use_container_width=True)


    except URLError as e:
        st.error(
            """
            *This demo requires internet access.*
            Connection error: %s
        """
            % e.reason
        )