# DELETES A STAFF MEMBER

import streamlit as st
from helper.functions import validate_id, delete_row

# only an administrator can remove a staff member
if "role" not in st.session_state or st.session_state.role != "Administrator":
    st.warning("ACCESS DENIED: You must be an Administrator to access this page.")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - Delete Staff", page_icon="🎬")  # sets page title and logo (on tab)
st.title("Delete Staff")
st.subheader("Remove a staff member")

# create a form for the user to fill out
with (st.form("delete_staff_form")):
    staffID = st.number_input("Staff ID", min_value=1, step=1)
    st.warning("BEWARE: You cannot undo this action.")
    submitted = st.form_submit_button("Remove Staff Member")
    if submitted:
        staff_exists = validate_id("Staff", "StaffID", staffID)

        if not staff_exists:
            st.error(f"Invalid Staff ID: {staffID}. Please check and try again.")
        else:
            delete_row("Staff", "StaffID", staffID)
            st.success("Staff member removed successfully!")
