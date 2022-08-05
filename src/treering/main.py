
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
from PIL import Image
import streamlit as st
import os
from util.pages.home_page import home_page
from util.pages.overview_page import overview_page
from util.pages.growth_index import growth_index
from util.pages.growth_index_period import growth_index_period
from util.pages.geo_location import geo_location
from util.pages.manage_data import manage_data_page
from util.pages.outliers import outliers



def get_current_dir():
    return os.getcwd()


def get_image_location():
    return os.path.join(get_current_dir(),"images")

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):

        im = Image.open(os.path.join(get_image_location(),"tab_tree.png"))
        st.set_page_config(page_title="TREE RING ANALYSIS", page_icon=im,layout="wide")

        st.sidebar.markdown("## Main Menu")
        app = st.sidebar.selectbox(
            "Select Page", self.apps, format_func=lambda app: app["title"]
        )
        st.sidebar.markdown("---")
        app["function"]()


app = MultiApp()

app.add_app("Home", home_page)
app.add_app("Overview", overview_page)
app.add_app("Outliers", outliers)
app.add_app("Growth Index By Spices", growth_index)
app.add_app("Growth Index By Geo Location", geo_location)
app.add_app("Growth Index By year", growth_index_period)
app.add_app("Manage Dataset", manage_data_page)


app.run()
