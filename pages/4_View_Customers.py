# SHOWS THE CUSTOMERS TABLE

import streamlit as st
from helper.functions import fetch_table_data

# only staff members can view all customers
if "role" not in st.session_state or st.session_state.role != "Staff":
    st.warning("ACCESS DENIED: You must be a Staff member to access this page.")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - View Customers", page_icon="🎬")   # sets page title and logo (on tab)
st.title("View Customers")
st.write()
st.subheader("Customers")

customers = fetch_table_data("Customers")
if not customers:
    st.write("No customers available.")
else:
    st.table(customers)
