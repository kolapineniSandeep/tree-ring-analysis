
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import streamlit as st

from util.pages.home_page import home_page
from util.pages.overview_page import overview_page
from util.pages.growth_index import growth_index
from util.pages.geo_location import geo_location



class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):

        st.set_page_config(page_title="TREE RING ANALYSIS", layout="wide")

        st.sidebar.markdown("## Main Menu")
        app = st.sidebar.selectbox(
            "Select Page", self.apps, format_func=lambda app: app["title"]
        )
        st.sidebar.markdown("---")
        app["function"]()


app = MultiApp()

app.add_app("Home", home_page)
app.add_app("Overview", overview_page)
app.add_app("Growth Index By Spices", growth_index)
app.add_app("Growth Index By Geo Location", geo_location)



app.run()
