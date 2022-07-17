
import streamlit as st
import webbrowser



def home_page():

    left_col, right_col = st.columns(2)


    right_col.markdown("# TREE RING ANALYSIS")
    right_col.markdown("### A tool for analyzing tree growth in canada")






    st.sidebar.markdown("## Reference Links")
    url = 'https://www.google.com/'
    if st.sidebar.button('Test Link'):
        webbrowser.open_new_tab(url)


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
        Sandeep Kolapineni
        
        
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

