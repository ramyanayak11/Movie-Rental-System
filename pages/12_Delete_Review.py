# DELETES A REVIEW

import streamlit as st
from helper.functions import connect_database, validate_id, delete_row

# only staff members can delete a movie
if "role" not in st.session_state or st.session_state.role != "Customer":
    st.warning("ACCESS DENIED: You must be a Customer to access this page.")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - Delete Review", page_icon="🎬")  # sets page title and logo (on tab)
st.title("Delete Review")
st.subheader("Delete a review")

# create a form for the user to fill out
with (st.form("delete_review_form")):
    custID = st.number_input("Your Customer ID", min_value=1, step=1)
    ratingID = st.number_input("Rating ID", min_value=1, step=1)
    st.warning("BEWARE: You cannot undo this action.")
    submitted = st.form_submit_button("Delete Review")
    if submitted:
        rating_exists = validate_id("Ratings", "RatingID", ratingID)
        customer_exists = validate_id("Customers", "CustomerID", custID)

        if not customer_exists:
            st.error(f"Invalid Customer ID: {ratingID}. Please check and try again.")
        if not rating_exists:
            st.error(f"Invalid Movie ID: {ratingID}. Please check and try again.")
        else:
            conn = connect_database()
            c = conn.cursor()

            c.execute(f"SELECT CustomerID FROM Ratings WHERE RatingID={ratingID}")
            originalAuthorID = c.fetchone()[0]

            if custID == originalAuthorID:  # customer can only delete reviews written by them
                delete_row("Ratings", "RatingID", ratingID)
                st.success("Review deleted successfully!")
            else:
                st.error("Customers can only delete reviews that were written by them. "
                         "You are not allowed to delete this review, as you are not the original author.")

            conn.close()
