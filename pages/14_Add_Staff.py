# ADDS A STAFF MEMBER

import streamlit as st
from helper.functions import connect_database

# only an administrator can add a staff member
if "role" not in st.session_state or st.session_state.role != "Administrator":
    st.warning("ACCESS DENIED: You must be an Administrator to access this page.")
    st.stop()

# add new customer function
def add_staff(name, email, phone, start_date):
    conn = connect_database()
    c = conn.cursor()

    c.execute(f"SELECT MAX(StaffID) FROM Staff")
    max_staffID = c.fetchone()[0]            # for setting staff id (= max staffID in the table + 1)

    c.execute('''
    INSERT INTO Staff (StaffID, StaffName, StaffEmail, StaffPhone, StartDate)
    VALUES (?, ?, ?, ?, ?)
    ''', (max_staffID + 1, name, email, phone, start_date))

    conn.commit()
    conn.close()


# UI details
st.set_page_config(page_title="Movie Rentals - Add Staff", page_icon="🎬")   # sets page title and logo (on tab)
st.title("Add Staff")
st.subheader("Add a new staff member")

# create a form for the user to fill out
with st.form("add_staff_form"):
    name = st.text_input("Staff Name")
    email = st.text_input("Staff Email")
    phone = st.text_input("Staff Phone")
    startDate = st.date_input("Start Date")
    submitted = st.form_submit_button("Add Staff Member")
    if submitted:
        if not name.strip():
            st.error("The staff name cannot be empty. Please enter a valid name.")
        elif not email.strip():
            st.error("The staff email cannot be empty. Please enter a valid email.")
        elif not phone.strip():
            st.error("The staff phone cannot be empty. Please enter a valid phone number.")
        else:
            add_staff(name.strip(), email.strip(), phone.strip(), startDate.strftime('%Y-%m-%d'))
            st.success(f"Staff member '{name}' added successfully!")
