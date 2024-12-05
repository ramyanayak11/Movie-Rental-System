# ADDS A NEW RENTAL ENTRY

import streamlit as st
from datetime import timedelta
from helper.functions import connect_database

# only staff members can add a rental
if "role" not in st.session_state or st.session_state.role != "Staff":
    st.warning("ACCESS DENIED: You must be a Staff member to access this page.")
    st.stop()

# add new rental data
def add_rental(movie_id, customer_id, rental_date, return_deadline):
    conn = connect_database()
    c = conn.cursor()

    c.execute(f"SELECT RentalRate FROM Movies WHERE MovieID = {movie_id}")  # gets rental rate
    rental_rate = c.fetchone()[0]

    c.execute(f"SELECT COUNT(*) FROM RentalRecords")
    row_count = c.fetchone()[0]                     # for rental id (= num rows in table + 1)

    c.execute('''
    INSERT INTO RentalRecords (RentalID, MovieID, CustomerID, RentalRate, RentalDate, ReturnDeadline)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (row_count + 1, movie_id, customer_id, rental_rate, rental_date, return_deadline))

    conn.commit()
    conn.close()


# UI details
st.set_page_config(page_title="Movie Rentals - Add Rental", page_icon="🎬")   # sets page title and logo (on tab)
st.title("Add Rental")
st.subheader("Add a new rental")

# create a form for the user to fill out
with st.form("add_rental_form"):
    movieID = st.number_input("Movie ID", min_value=1, step=1)
    custID = st.number_input("Customer ID", min_value=1, step=1)
    rentalDate = st.date_input("Date Rented")
    submitted = st.form_submit_button("Add Rental")
    if submitted:
        returnDeadline = rentalDate + timedelta(days=7)  # return deadline is 7 days after rented out
        add_rental(movieID, custID, rentalDate.strftime('%Y-%m-%d'), returnDeadline.strftime('%Y-%m-%d'))
        st.success(f"Rental added successfully!")
