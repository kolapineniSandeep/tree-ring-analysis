import streamlit as st
import webbrowser
import pandas as pd
import numpy as np
from urllib.error import URLError
import altair as alt


def home_page():
    left_col, right_col = st.columns(2)

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

    @st.cache
    def get_UN_data():
        df = pd.read_csv("src/treering/OpenData/detrend v0.1.1 a.csv")
        df.rename(columns={'res.Lbai.normalized': 'growth_index'}, inplace=True)
        df.drop(["uid_tree", "uid_radius", "SummerSMI", "SummerSMI.t_1", "Ecoregions"], axis=1, inplace=True)
        df = df.groupby(['species', 'year'], as_index=False)['growth_index'].mean()
        df = df.pivot(index='species', columns='year', values='growth_index')
        df = df.replace(np.nan, 0)
        df.columns = df.columns.astype(str)
        return df

    with right_info_col:
        try:
            df = get_UN_data()
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
