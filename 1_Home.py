# HOME PAGE

import streamlit as st
from helper.functions import create_tables, add_sample_data

create_tables()     # initialize tables
add_sample_data()   # add sample data

# UI details
st.set_page_config(page_title="Movie Rentals - Home", page_icon="🎬")   # sets page title and logo (on tab)
st.subheader("Welcome to the Movie Rental System.")
st.write("")


# select role (customer/staff), which determines access to pages

if "role" not in st.session_state:
    st.session_state.role = "Select Role"

role = st.selectbox(        # selection retains prev selected option
    "Select Role",
    ["Select Role", "Customer", "Staff"],
    index=["Select Role", "Customer", "Staff"].index(st.session_state.role),
)

if role != "Select Role":   # prints selection confirmation
    st.session_state['role'] = role
    st.success(f"Selected Role: {st.session_state['role']}")
else:
    st.write("Please select a role to proceed.")
