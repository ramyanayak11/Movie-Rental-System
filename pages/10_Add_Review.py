# ADDS A NEW REVIEW
import streamlit as st
from helper.functions import connect_database

# only customers can add a review
if "role" not in st.session_state or st.session_state.role != "Customer":
    st.warning("ACCESS DENIED: You must be a Customer to access this page.")
    st.stop()

# add new customer rating
def add_rating(customer_id, movie_id, rating_score, review, date):
    conn = connect_database()
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM Ratings")
    row_count = c.fetchone()[0]  # for rating id (= num rows in table + 1)

    c.execute('''
    INSERT INTO Ratings (RatingID, MovieID, CustomerID, RatingScore, Review, RatingDate)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (row_count + 1, movie_id, customer_id, rating_score, review, date))

    conn.commit()
    conn.close()


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
        add_rating(custID, movieID, rating, review, date.strftime('%Y-%m-%d'))
        st.success(f"Review added successfully!")
