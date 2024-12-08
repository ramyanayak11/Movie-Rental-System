# ADDS A NEW REVIEW

import streamlit as st
from helper.functions import connect_database, validate_id, create_menu

# only customers can add a review
if "role" not in st.session_state or st.session_state.role != "Customer":
    st.warning("ACCESS DENIED: You must be a Customer to access this page.")
    if st.button("Go Back"):
        st.switch_page("pages/10_View_Reviews.py")
    st.stop()

# add new customer rating
def add_rating(customer_id, movie_id, rating_score, review, date):
    try:
        conn = connect_database()
        c = conn.cursor()

        c.execute("SELECT MAX(RatingID) FROM Ratings")
        max_ratingID = c.fetchone()[0]  # for setting rating id (= max ratingID in the table + 1)
                                        # uses MAX instead of COUNT to avoid conflicts with deletion

        c.execute('''
        INSERT INTO Ratings (RatingID, MovieID, CustomerID, RatingScore, Review, RatingDate)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (max_ratingID + 1, movie_id, customer_id, rating_score, review, date))

        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error adding review: {e}")

# UI details
st.set_page_config(page_title="Movie Rentals - Add Review", page_icon="🎬",  layout="wide", initial_sidebar_state="collapsed")  # sets page title and logo (on tab)
create_menu()
st.title("Add Review")
st.subheader("Add a new review")

# create a form for the user to fill out
with st.form("add_rating_form"):
    custID = st.number_input("Customer ID", min_value=1, step=1)
    movieID = st.number_input("Movie ID", min_value=1, step=1)
    rating = st.number_input("Rating Score", min_value=1, step=1, max_value=10)
    review = st.text_input("Review")
    date = st.date_input("Date of Review")
    submitted = st.form_submit_button("Add Review")
    if submitted:
        if not review.strip():  # Check if the review is empty or only contains whitespace
            st.error("The review field cannot be empty. Please provide your feedback.")
        else:
            customer_exists = validate_id("Customers", "CustomerID", custID)
            movie_exists = validate_id("Movies", "MovieID", movieID)
            
            if not customer_exists:
                st.error(f"Invalid Customer ID: {custID}. Please check and try again.")
            elif not movie_exists:
                st.error(f"Invalid Movie ID: {movieID}. Please check and try again.")
            else:
                add_rating(custID, movieID, rating, review, date.strftime('%Y-%m-%d'))
                st.success("Review added successfully!")

# Return to View Reviews button
if st.button("🔙 Return to View Reviews"):
    st.query_params.update(page="View_Reviews", role=st.session_state.role)
    st.switch_page("pages/10_View_Reviews.py")
