# ADDS A CUSTOMER

import streamlit as st
from helper.functions import connect_database

# only staff members can add a customer
if "role" not in st.session_state or st.session_state.role != "Staff":
    st.warning("ACCESS DENIED: You must be a Staff member to access this page.")
    st.stop()

# add new customer function
def add_customer(name, email, phone):
    conn = connect_database()
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM Customers")
    row_count = c.fetchone()[0]                     # for customer id (= num rows in table + 1)

    c.execute('''
    INSERT INTO Customers (CustomerID, CustomerName, CustomerEmail, CustomerPhone)
    VALUES (?, ?, ?, ?)
    ''', (row_count + 1, name, email, phone))

    conn.commit()
    conn.close()


# UI details
st.set_page_config(page_title="Movie Rentals - Add Customer", page_icon="🎬")   # sets page title and logo (on tab)
st.title("Add Customer")
st.subheader("Add a new customer")

# create a form for the user to fill out
with st.form("add_customer_form"):
    name = st.text_input("Customer Name")
    email = st.text_input("Customer Email")
    phone = st.text_input("Customer Phone")
    submitted = st.form_submit_button("Add Customer")
    if submitted:
        add_customer(name, email, phone)
        st.success(f"Customer '{name}' added successfully!")
