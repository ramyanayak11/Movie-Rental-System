# SHOWS THE RATINGS TABLE
# ALONG WITH JOIN ON MOVIES TO GET MOVIE NAMES

import streamlit as st
from helper.functions import fetch_table_data

# UI details
st.set_page_config(page_title="Movie Rentals - View Reviews", page_icon="🎬")   # sets page title and logo (on tab)
st.title("View Reviews")
st.write()
st.subheader("Reviews")

ratings = fetch_table_data("Ratings", False, True)
if not ratings:
    st.write("No ratings/reviews available.")
else:
    st.table(ratings)
