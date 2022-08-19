
import streamlit as st
from PIL import Image
import os
import numpy as np
from ..scripts.data_pool import my_data
from typing import List, Optional
import markdown
from urllib.error import URLError
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, KernelPCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

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


#@st.cache()
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


@st.cache()
def get_data_province():
    df_province = my_data().get_data_with_province()

    return df_province


def overview_page():
    get_data()

    st.markdown("## Summary of the Tree Ring Analysis")

    st.markdown("""
    #### The tree ring analysis database is a collection of 1,633,826 instances spanning over 67 years containing 47 projects and samples from 66 species of trees
    """)
    "====================================METRICS ROW 1==============================================================="
    st.markdown("---")
    total_year = f'{min_year} to {max_year}'
    with Grid("1 1 1") as grid:
        grid.cell(
            class_="a",
            grid_column_start=2,
            grid_column_end=3,
            grid_row_start=1,
            grid_row_end=2,
        ).markdown("## YEARS<br/>"+(total_year))
        grid.cell("b", 2, 3, 2, 3).markdown("## TOTAL SITES <br/><h1>"+str(total_sites)+"</h1>")
        grid.cell("c", 3, 4, 2, 3).markdown("## TOTAL SPICES<br/><h1>"+str(total_species)+"</h1>")
        grid.cell("d", 1, 2, 1, 2).markdown("## TOTAL TREES <br/><h1>"+str(total_trees)+"</h1>")
        grid.cell("f", 1, 2, 2, 3).markdown("## TOTAL INSTANCES <br/><h1>"+str(total_instances)+"</h1>")

        grid.cell("e", 3, 4, 1, 2).markdown("## TOTAL CONTRIBUTORS<br/><h1>"+str(total_projects)+"</h1>")



    ''' =======================================CLUSTERING========================================================'''
    df_prov = get_data_province()

    tr_df2 = df_prov.groupby(['uid_site', 'species', 'year', 'state'], as_index=False)[
        ['growth_index']].mean()

    tr_df3 = tr_df2.pivot_table(index=["uid_site", "species", "state"], columns="year", values="growth_index",
                                fill_value=0)
    tr_df3.reset_index(inplace=True)
    tr_df3_copy = tr_df3.copy()

    # Label Encoding
    le = LabelEncoder()
    tr_df3['species'] = le.fit_transform(tr_df3['species'])
    tr_df3['state'] = le.fit_transform(tr_df3['state'])

    # Standar Scaler
    features = StandardScaler().fit_transform(tr_df3.values)

    # PCA Principal componente Analysis
    pca = PCA(n_components=5, whiten=True)
    features_pca = pca.fit_transform(features)


    kmeans = KMeans(n_clusters=6,
                    init='k-means++',
                    random_state=42).fit(features_pca)

    labels = kmeans.labels_

    tr_df3['Cluster'] = labels
    tr_df3_copy['Cluster'] = labels
    y_kmeans = kmeans.fit_predict(features)

    '''==============================Clustering Evaluation Metrics===================================================='''
    se = silhouette_score(features_pca, labels)
    ch = calinski_harabasz_score(features_pca, labels)
    db = davies_bouldin_score(features_pca, labels)

    '''==============================3D Scatter Plot=================================================================='''
    # 3d scatter plot using plotly
    Scene = dict(xaxis=dict(title='Period-->'), yaxis=dict(title='Growth Index--->'),
                 zaxis=dict(title='Species_Site-->'))

    u_labels = np.unique(labels)
    data_trace = []
    colors = ['blue', 'orange', 'green', 'yellow', 'red', 'magenta']

    for i in u_labels:
        trace = go.Scatter3d(x=features_pca[labels == i, 0],
                             y=features_pca[labels == i, 1],
                             z=features_pca[labels == i, 2],
                             name='Cluster ' + str(i),
                             mode='markers',
                             marker=dict(color=colors[i], size=10, line=dict(color='black', width=10)))

        data_trace.append(trace)

    layout = go.Layout(margin=dict(l=0, r=0), scene=Scene, height=1000, width=1000)
    fig = go.Figure(data=data_trace, layout=layout)
    fig.update_layout(legend={"title": "Clusters"})
    '''==============================================================================================================='''

    # countplot to check the number of clusters and number of customers in each cluster
    cv_data = Counter(kmeans.labels_).items()
    cv_df = pd.DataFrame.from_dict(cv_data)
    cv_df = cv_df.rename(columns={0: "cluster", 1: "value"})
    #cv_df.sort_values(by=['cluster'], ascending=False)

    fig2 = px.bar(cv_df, x='value', y='cluster', color='cluster', orientation='h', height=500,
                 text_auto=True)

    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis={'categoryorder':'total descending'})

    st.markdown("-------------------------")
    col1, col2 = st.columns([3,2])

    with col1:
        st.header("3D Clustering ")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.header("Total instances per cluster ")
        st.plotly_chart(fig2)

        st.write('## Evaluation metrics')
        st.markdown('-------')
        col2.metric('Silhouette Coefficient', round(se, 6))
        col2.metric('Calinski Harabasz', round(ch, 4))
        col2.metric('Daviews Bouldin', round(db, 4))

    st.markdown("-------------------------")


    st.write("### Filter Data by Cluster")
    st.dataframe(tr_df3_copy)
    # try:
    #     tr_df3_copy = tr_df3_copy.set_index('Cluster')
    #     clusters = st.multiselect(
    #         "Choose cluster", list(tr_df3_copy.index.unique()),[0]
    #     )
    #     if not clusters:
    #         st.error("Please select at least one specie.")
    #     else:
    #         data = tr_df3_copy.loc[clusters]
    #         data = data.reset_index()
    #         data = data.set_index('state')
    #
    #         provinces = st.multiselect(
    #             "Choose Province/Region", list(data.index.unique()),
    #             ['Alberta', 'Saskatchewan', 'British Columbia', 'Ontario', 'Northwest Territories', 'Yukon', 'Manitoba']
    #         )
    #         if not provinces:
    #             st.error("Please select at least one province.")
    #
    #         else:
    #             data = data.loc[provinces]
    #             data = data.reset_index()
    #             st.dataframe(data)
    # except URLError as e:
    #     st.error(
    #         """
    #         *This demo requires internet access.*
    #         Connection error: %s
    #         """
    #             % e.reason
    #         )




class Cell:
    """A Cell can hold text, markdown, plots etc."""
    def __init__(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        self.class_ = class_
        self.grid_column_start = grid_column_start
        self.grid_column_end = grid_column_end
        self.grid_row_start = grid_row_start
        self.grid_row_end = grid_row_end
        self.inner_html = ""

    def _to_style(self) -> str:
        return f"""
.{self.class_} {{
    grid-column-start: {self.grid_column_start};
    grid-column-end: {self.grid_column_end};
    grid-row-start: {self.grid_row_start};
    grid-row-end: {self.grid_row_end};
}}
"""

    def text(self, text: str = ""):
        self.inner_html = text

    def markdown(self, text):
        self.inner_html = markdown.markdown(text)



    def to_html(self):
        return f"""<div class="box {self.class_}">{self.inner_html}</div>"""


class Grid:
    """A (CSS) Grid"""
    def __init__(
        self, template_columns="1 1 1", gap="10px", background_color="white", color="#cbd5e8"
    ):
        self.template_columns = template_columns
        self.gap = gap
        self.background_color = background_color
        self.color = color
        self.cells: List[Cell] = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        st.markdown(self._get_grid_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_html(), unsafe_allow_html=True)

    def _get_grid_style(self):
        return f"""
<style>
    .wrapper {{
    display: grid;
    grid-template-columns: {self.template_columns};
    grid-gap: {self.gap};
    background-color: {self.background_color};
    color: {self.color};
    }}
    .box {{
    background-color: {self.color};
    color: {self.background_color};
    border-radius: 5px;
    padding: 20px;
    font-size: 150%;
    }}
    table {{
        color: {self.color}
    }}
</style>
"""

    def _get_cells_style(self):
        return (
            "<style>" + "\n".join([cell._to_style() for cell in self.cells]) + "</style>"
        )

    def _get_cells_html(self):
        return (
            '<div class="wrapper">'
            + "\n".join([cell.to_html() for cell in self.cells])
            + "</div>"
        )

    def cell(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        cell = Cell(
            class_=class_,
            grid_column_start=grid_column_start,
            grid_column_end=grid_column_end,
            grid_row_start=grid_row_start,
            grid_row_end=grid_row_end,
        )
        self.cells.append(cell)
        return cell
