# HOME PAGE

import streamlit as st
from helper.functions import create_tables, add_sample_data, create_menu

create_tables()     # initialize tables
add_sample_data()   # add sample data

# UI details
st.set_page_config(page_title="Movie Rentals - Home", page_icon="🎬", layout="wide", initial_sidebar_state="collapsed", menu_items=None)   # sets page title and logo (on tab)
create_menu() # menu button
st.subheader("Welcome to the Movie Rental System.")
st.write("")

# select role (customer/staff), which determines access to pages
if "role" not in st.session_state:
    st.session_state.role = "Select Role"

role = st.selectbox(        # selection retains prev selected option
    "Select Role",
    ["Select Role", "Customer", "Staff", "Administrator"],
    index=["Select Role", "Customer", "Staff", "Administrator"].index(st.session_state.role),
)

if role != "Select Role":   # prints selection confirmation
    st.session_state['role'] = role
    st.success(f"Selected Role: {st.session_state['role']}")
    st.write(" ")
    st.write("You can proceed by selecting any page from the navigation menu on the left.")
else:
    st.write("Please select a role to proceed.")
