# DELETES A MOVIE

import streamlit as st
from helper.functions import validate_id, delete_row

# only staff members or administrators can delete a movie
if "role" not in st.session_state or (st.session_state.role != "Staff" and st.session_state.role != "Administrator"):
    st.warning("ACCESS DENIED: You must be a Staff member or an Administrator to access this page.")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - Delete Movie", page_icon="🎬")  # sets page title and logo (on tab)
st.title("Delete Movie")
st.subheader("Delete a movie")

# create a form for the user to fill out
with (st.form("delete_movie_form")):
    movieID = st.number_input("Movie ID", min_value=1, step=1)
    st.warning("BEWARE: You cannot undo this action.")
    submitted = st.form_submit_button("Delete Movie")
    if submitted:
        movie_exists = validate_id("Movies", "MovieID", movieID)

        if not movie_exists:
            st.error(f"Invalid Movie ID: {movieID}. Please check and try again.")
        else:
            delete_row("Movies", "MovieID", movieID)
            st.success("Movie deleted successfully!")
