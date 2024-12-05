# SHOWS THE MOVIES TABLE

import streamlit as st
from helper.functions import fetch_table_data

# UI details
st.set_page_config(page_title="Movie Rentals - View Movies", page_icon="🎬")   # sets page title and logo (on tab)
st.title("View Movies")
st.write()
st.subheader("Movies")

movies = fetch_table_data("Movies")

if not movies:
    st.write("No movies available.")
else:
    st.table(movies)
