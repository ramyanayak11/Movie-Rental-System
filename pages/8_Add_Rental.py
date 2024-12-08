# ADDS A NEW RENTAL ENTRY

import streamlit as st
from datetime import timedelta
from helper.functions import create_menu, connect_database, validate_id

# only staff members or administrators can add a rental
if "role" not in st.session_state or (st.session_state.role != "Staff" and st.session_state.role != "Administrator"):
    st.warning("ACCESS DENIED: You must be a Staff member or an Administrator to access this page.")
    if st.button("Go back to Home"):
        st.switch_page("1_Home.py")
    st.stop()

# add new rental data
def add_rental(movie_id, customer_id, rental_date, return_deadline):
    try:
        conn = connect_database()
        c = conn.cursor()

        c.execute("SELECT RentalRate FROM Movies WHERE MovieID = ?", (movie_id,))
        rental_rate = c.fetchone()[0]

        c.execute("SELECT MAX(RentalID) FROM RentalRecords")
        max_rentalID = c.fetchone()[0]  # for setting rental id (= max rental in the table + 1)

        c.execute('''
        INSERT INTO RentalRecords (RentalID, MovieID, CustomerID, RentalRate, RentalDate, ReturnDeadline)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (max_rentalID + 1, movie_id, customer_id, rental_rate, rental_date, return_deadline))

        conn.commit()
        conn.close()
        return rental_rate
    except Exception as e:
        st.error(f"Error adding rental: {e}")
        return None

# UI details
st.set_page_config(page_title="Movie Rentals - Add Rental", page_icon="🎬",  layout="wide", initial_sidebar_state="collapsed")   # sets page title and logo (on tab)
create_menu()
st.title("Add Rental")
st.subheader("Add a new rental")

# create a form for the user to fill out
with st.form("add_rental_form"):
    movieID = st.number_input("Movie ID", min_value=1, step=1)
    custID = st.number_input("Customer ID", min_value=1, step=1)
    rentalDate = st.date_input("Date Rented")
    submitted = st.form_submit_button("Add Rental")
    if submitted:
        customer_exists = validate_id("Customers", "CustomerID", custID)
        movie_exists = validate_id("Movies", "MovieID", movieID)
        
        if not movie_exists:
            st.error(f"Invalid Movie ID: {movieID}. Please check and try again.")
        elif not customer_exists:
            st.error(f"Invalid Customer ID: {custID}. Please check and try again.")
        else:
            returnDeadline = rentalDate + timedelta(days=7)  # return deadline is 7 days after rented out
            rental_rate = add_rental(movieID, custID, rentalDate.strftime('%Y-%m-%d'), returnDeadline.strftime('%Y-%m-%d'))
            if rental_rate:
                st.success("Rental added successfully!")
                st.markdown(f"""
                **Reminder:**
                - Customer should return the movie by **{returnDeadline}** to avoid late fees.
                - The rental fee is **${rental_rate:.2f}**.
                - Late fees are **$0.50 per day** beyond the return deadline.
                """)
# Return to View Rentals button
if st.button("🔙 Return to View Rentals"):
    st.query_params.update(page="View_Rentals", role=st.session_state.role)
    st.switch_page("pages/7_View_Rentals.py")
