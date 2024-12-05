# PROCESSES THE RETURN OF A RENTAL

import streamlit as st
from datetime import datetime
from helper.functions import connect_database

# only staff members can return a rental
if "role" not in st.session_state or st.session_state.role != "Staff":
    st.warning("ACCESS DENIED: You must be a Staff member to access this page.")
    st.stop()

# Updates rental when movie is returned
def return_rental(rental_id, return_date):
    conn = connect_database()
    c = conn.cursor()

    late_fee = 0.0

    c.execute(f"SELECT RentalRate, ReturnDeadline FROM RentalRecords WHERE RentalID = {rental_id}")  # gets rental deadline
    result = c.fetchone()
    rate = result[0]
    rDeadline = result[1]

    rDeadline = datetime.strptime(rDeadline, '%Y-%m-%d')  # convert dates to datetime
    rDate = datetime.strptime(return_date, '%Y-%m-%d')  # objects for comparison

    if rDate > rDeadline:  # calculate late fee if returned after deadline
        late_days = (rDate - rDeadline).days
        late_fee = late_days * 0.50  # $0.50 per day late

    c.execute('''
        UPDATE RentalRecords
        SET ReturnDate = ?, LateFee = ?, TotalPayment = ?
        WHERE RentalID = ?
        ''', (return_date, late_fee, rate+late_fee, rental_id))

    conn.commit()
    conn.close()


# UI details
st.set_page_config(page_title="Movie Rentals - Return Rental", page_icon="🎬")  # sets page title and logo (on tab)
st.title("Return Rental")
st.subheader("Return a rental")

# create a form for the user to fill out
with st.form("return_rental_form"):
    rentalID = st.number_input("Rental ID", min_value=1, step=1)
    returnDate = st.date_input("Date Returned")

    submitted = st.form_submit_button("Return Rental")
    if submitted:
        return_rental(rentalID, returnDate.strftime('%Y-%m-%d'))
        st.success(f"Rental returned successfully!")
