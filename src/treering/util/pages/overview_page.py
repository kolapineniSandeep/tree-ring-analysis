import streamlit
import streamlit as st
from PIL import Image
import os
import numpy as np
from ..scripts.data_pool import my_data
from typing import List, Optional
import markdown


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
        grid.cell("d", 1, 2, 1, 3).markdown("## TOTAL TREES <br/><h1>"+str(total_trees)+"</h1>")

        grid.cell("e", 3, 4, 1, 2).markdown("## TOTAL CONTRIBUTORS<br/><h1>"+str(total_projects)+"</h1>")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    #col1.metric(label="Total Tress", value=total_trees, delta="1.2 °F")
    #col1.metric(label="Total Trees", value= "{:,}".format(total_trees))
    ##col5.metric(label='Total Instances', value= "{:,}".format(total_instances))

    "====================================METRICS ROW 2==============================================================="
    st.image(im2, caption='')

    # left_col.image(im2, caption='')
    # left_col.markdown("""## 4471""")
    # left_col.markdown(" sites where observed and recorded for the data")
    #
    # ## Right Side
    # right_col.markdown("""## 66 """)
    # right_col.markdown("species where analysed for their growth patterns")

## ADD CLUSTER















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
