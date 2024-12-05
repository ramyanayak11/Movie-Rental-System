# ADDS A NEW REVIEW
import streamlit as st
from helper.functions import connect_database

# only customers can add a review
if "role" not in st.session_state or st.session_state.role != "Customer":
    st.warning("ACCESS DENIED: You must be a Customer to access this page.")
    st.stop()

# validate customer ID and movie ID
def validate_ids(customer_id, movie_id):
    try:
        conn = connect_database()
        c = conn.cursor()
        
        # Check if the CustomerID exists
        c.execute("SELECT COUNT(*) FROM Customers WHERE CustomerID = ?", (customer_id,))
        customer_exists = c.fetchone()[0] > 0
        
        # Check if the MovieID exists
        c.execute("SELECT COUNT(*) FROM Movies WHERE MovieID = ?", (movie_id,))
        movie_exists = c.fetchone()[0] > 0
        
        conn.close()
        return customer_exists, movie_exists
    except Exception as e:
        st.error(f"Error validating IDs: {e}")
        return False, False

# add new customer rating
def add_rating(customer_id, movie_id, rating_score, review, date):
    try:
        conn = connect_database()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM Ratings")
        row_count = c.fetchone()[0]  # for rating id (= num rows in table + 1)

        c.execute('''
        INSERT INTO Ratings (RatingID, MovieID, CustomerID, RatingScore, Review, RatingDate)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (row_count + 1, movie_id, customer_id, rating_score, review, date))

        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error adding review: {e}")

# UI details
st.set_page_config(page_title="Movie Rentals - Add Review", page_icon="🎬")  # sets page title and logo (on tab)
st.title("Add Review")
st.subheader("Add a new review")

# create a form for the user to fill out
with st.form("add_rating_form"):
    custID = st.number_input("Customer ID", min_value=1, step=1)
    movieID = st.number_input("Movie ID", min_value=1, step=1)
    rating = st.number_input("Rating Score", min_value=1.0, step=0.1, max_value=10.0)
    review = st.text_input("Review")
    date = st.date_input("Date of Review")
    submitted = st.form_submit_button("Add Review")
    if submitted:
        if not review.strip():  # Check if the review is empty or only contains whitespace
            st.error("The review field cannot be empty. Please provide your feedback.")
        else:
            customer_exists, movie_exists = validate_ids(custID, movieID)
            
            if not customer_exists:
                st.error(f"Invalid Customer ID: {custID}. Please check and try again.")
            elif not movie_exists:
                st.error(f"Invalid Movie ID: {movieID}. Please check and try again.")
            else:
                add_rating(custID, movieID, rating, review, date.strftime('%Y-%m-%d'))
                st.success("Review added successfully!")
