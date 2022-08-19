
import streamlit as st
from PIL import Image
import os
import numpy as np
from ..scripts.data_pool import my_data
from typing import List, Optional
import markdown

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, KernelPCA
from sklearn.cluster import KMeans
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

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

#@st.cache()
def get_data_cluster():
    df_cluster = my_data().get_data_for_cluster()

    return df_cluster



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
    df_cl = get_data_cluster()
    df_cl.drop(["Cluster"], axis=1, inplace=True)

    ##st.dataframe(df_cl)

    le = LabelEncoder()
    pca = PCA(n_components=30, whiten=True)

    df_cl['species'] = le.fit_transform(df_cl['species'])
    df_cl['state'] = le.fit_transform(df_cl['state'])

    features = StandardScaler().fit_transform(df_cl.values)
    features_pca = pca.fit_transform(features)

    kmeans = KMeans(n_clusters=5,
                    init='k-means++',
                    random_state=0).fit(features_pca)

    labels = kmeans.labels_
    y_kmeans = kmeans.fit_predict(features)

    # 3d scatter plot using plotly
    Scene = dict(xaxis=dict(title='Period-->'), yaxis=dict(title='Growth Index--->'),
                 zaxis=dict(title='Species_Site-->'))

    cluster1 = go.Scatter3d(x=features_pca[labels == 0, 0],
                            y=features_pca[labels == 0, 1],
                            z=features_pca[labels == 0, 2],
                            name='Cluster1',
                            mode='markers',
                            marker=dict(color='blue', size=10, line=dict(color='black', width=10))
                            )

    cluster2 = go.Scatter3d(x=features_pca[labels == 1, 0],
                            y=features_pca[labels == 1, 1],
                            z=features_pca[labels == 1, 2],
                            name='Cluster2',
                            mode='markers',
                            marker=dict(color='orange', size=10, line=dict(color='black', width=10))
                            )

    cluster3 = go.Scatter3d(x=features_pca[labels == 2, 0],
                            y=features_pca[labels == 2, 1],
                            z=features_pca[labels == 2, 2],
                            name='Cluster3',
                            mode='markers',
                            marker=dict(color='green', size=10, line=dict(color='black', width=10))
                            )

    cluster4 = go.Scatter3d(x=features_pca[labels == 3, 0],
                            y=features_pca[labels == 3, 1],
                            z=features_pca[labels == 3, 2],
                            name='Cluster4',
                            mode='markers',
                            marker=dict(color='yellow', size=10, line=dict(color='black', width=10))
                            )

    cluster5 = go.Scatter3d(x=features_pca[labels == 4, 0],
                            y=features_pca[labels == 4, 1],
                            z=features_pca[labels == 4, 2],
                            name='Cluster5',
                            mode='markers',
                            marker=dict(color='#D12B60', size=10, line=dict(color='black', width=10))
                            )

    layout = go.Layout(margin=dict(l=0, r=0), scene=Scene, height=1000, width=1000)
    data = [cluster1, cluster2, cluster3, cluster4, cluster5]


    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(legend={"title": "Clusters"})

    # countplot to check the number of clusters and number of customers in each cluster
    fig2 = plt.figure(figsize=(10, 4))
    ax = sns.countplot(y_kmeans)

    for p in ax.patches:
        ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x() + 0.1, p.get_height() + 50))


    st.markdown("-------------------------")

    st.header("3D Clustering ")
    st.plotly_chart(fig, use_container_width=True)

    st.header("Total instances per cluster ")
    st.pyplot(fig2)






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
