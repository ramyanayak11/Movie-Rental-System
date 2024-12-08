# PROCESSES THE RETURN OF A RENTAL

import streamlit as st
from datetime import datetime
from helper.functions import connect_database

# only staff members or administrators can return a rental
if "role" not in st.session_state or (st.session_state.role != "Staff" and st.session_state.role != "Administrator"):
    st.warning("ACCESS DENIED: You must be a Staff member or an Administrator to access this page.")
    st.stop()

# Updates rental when movie is returned
def return_rental(rental_id, return_date):
    conn = None
    try:
        conn = connect_database()
        c = conn.cursor()

        # Retrieve rental details
        c.execute("SELECT RentalRate, ReturnDeadline, ReturnDate FROM RentalRecords WHERE RentalID = ?", (rental_id,))
        result = c.fetchone()

        if not result:
            raise ValueError(f"Rental ID {rental_id} is invalid or does not exist.")

        rate, rDeadline, rDate = result

        # Check if rental has already been returned
        if rDate is not None:
            raise ValueError(f"Rental ID {rental_id} has already been returned on {rDate}.")

        # Convert dates to datetime for comparison
        rDeadline = datetime.strptime(rDeadline, '%Y-%m-%d')
        rDate = datetime.strptime(return_date, '%Y-%m-%d')

        # Calculate late fee if returned after deadline
        late_fee = 0.0
        if rDate > rDeadline:
            late_days = (rDate - rDeadline).days
            late_fee = late_days * 0.50  # $0.50 per day late

        # Update rental record
        c.execute('''
            UPDATE RentalRecords
            SET ReturnDate = ?, LateFee = ?, TotalPayment = ?
            WHERE RentalID = ?
            ''', (return_date, late_fee, rate + late_fee, rental_id))

        conn.commit()
        return True  # Return True if the rental was processed successfully

    except ValueError as ve:
        st.error(str(ve))
        return False  # Return False if the rental ID is invalid or already returned
    except Exception as e:
        st.error(f"An error occurred while processing the return: {e}")
        return False  # Return False in case of other errors
    finally:
        # Ensure the connection is closed safely
        if conn:
            try:
                conn.close()
            except Exception as e:
                st.error(f"Error closing the connection: {e}")

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
        # Ensure rental ID is provided
        if rentalID <= 0:
            st.error("Please provide a valid Rental ID.")
        else:
            if return_rental(rentalID, returnDate.strftime('%Y-%m-%d')):
                st.success("Rental returned successfully!")

