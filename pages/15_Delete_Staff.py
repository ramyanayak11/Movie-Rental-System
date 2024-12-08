# DELETES A STAFF MEMBER

import streamlit as st
from helper.functions import validate_id, delete_row, create_menu

# only an administrator can remove a staff member
if "role" not in st.session_state or st.session_state.role != "Administrator":
    st.warning("ACCESS DENIED: You must be an Administrator to access this page.")
    if st.button("Go Back"):
        st.switch_page("pages/13_View_Staff.py")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - Delete Staff", page_icon="🎬",  layout="wide", initial_sidebar_state="collapsed")  # sets page title and logo (on tab)
create_menu()
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

# Return to View Staff button
if st.button("🔙 Return to View Staff"):
    st.query_params.update(page="View_Staff", role=st.session_state.role)
    st.switch_page("pages/13_View_Staff.py")
