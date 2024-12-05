# ADDS A MOVIE

import streamlit as st
from helper.functions import connect_database

# only staff members can add a movie
if "role" not in st.session_state or st.session_state.role != "Staff":
    st.warning("ACCESS DENIED: You must be a Staff member to access this page.")
    st.stop()

# add new movie function
def add_movie(title, release_date, genre, length, rental_rate):
    conn = connect_database()
    c = conn.cursor()

    c.execute(f"SELECT COUNT(*) FROM Movies")
    row_count = c.fetchone()[0]  # for movie id (= num rows in table + 1)

    c.execute('''
    INSERT INTO Movies (MovieID, MovieTitle, ReleaseDate, Genre, Length, RentalRate)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (row_count + 1, title, release_date, genre, length, rental_rate))

    conn.commit()
    conn.close()


# UI details
st.set_page_config(page_title="Movie Rentals - Add Movie", page_icon="🎬")   # sets page title and logo (on tab)
st.title("Add Movie")
st.subheader("Add a new movie")

# create a form for the user to fill out
with st.form("add_movie_form"):
    title = st.text_input("Movie Title")
    release_date = st.date_input("Release Date")
    genre = st.text_input("Genre")
    length = st.number_input("Length (in minutes)", min_value=1, step=1)
    rental_rate = st.number_input("Rental Rate ($)", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Movie")
    if submitted:
        add_movie(title, release_date.strftime('%Y-%m-%d'), genre, int(length), float(rental_rate))
        st.success(f"Movie '{title}' added successfully!")