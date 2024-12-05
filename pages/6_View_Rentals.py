# SHOWS THE RENTALS TABLE
# ALONG WITH JOIN ON MOVIES TO GET MOVIE NAMES

import streamlit as st
from helper.functions import fetch_table_data

# only staff members can view rental records
if "role" not in st.session_state or st.session_state.role != "Staff":
    st.warning("ACCESS DENIED: You must be a Staff member to access this page.")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - View Rentals", page_icon="🎬")   # sets page title and logo (on tab)
st.title("View Rentals")
st.write()
st.subheader("Rentals")

rentals = fetch_table_data("RentalRecords", True)
if not rentals:
    st.write("No rental records available.")
else:
    st.table(rentals)
