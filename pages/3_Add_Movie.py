# ADDS A MOVIE

import streamlit as st
from helper.functions import connect_database, create_menu

# only staff members or administrators can add a movie
if "role" not in st.session_state or (st.session_state.role != "Staff" and st.session_state.role != "Administrator"):
    st.warning("ACCESS DENIED: You must be a Staff member or an Administrator to access this page.")
    if st.button("Go Back"):
        st.switch_page("pages/2_View_Movies.py") 
    st.stop()

# add new movie function
def add_movie(title, release_date, genre, length, rental_rate):
    conn = connect_database()
    c = conn.cursor()

    c.execute(f"SELECT MAX(MovieID) FROM Movies")
    max_movieID = c.fetchone()[0]   # for setting movie id (= max movieID in the table + 1)
                                    # uses MAX instead of COUNT to avoid conflicts with deletion

    c.execute('''
    INSERT INTO Movies (MovieID, MovieTitle, ReleaseDate, Genre, Length, RentalRate)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (max_movieID + 1, title, release_date, genre, length, rental_rate))

    conn.commit()
    conn.close()


# UI details
st.set_page_config(page_title="Movie Rentals - Add Movie", page_icon="🎬",  layout="wide", initial_sidebar_state="collapsed")   # sets page title and logo (on tab)
create_menu()
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
        if not title.strip():
            st.error("The movie title cannot be empty. Please enter a valid title.")
        elif not genre.strip():
            st.error("The genre field cannot be empty. Please enter a valid genre.")
        else:
            add_movie(title, release_date.strftime('%Y-%m-%d'), genre, int(length), float(rental_rate))
            st.success(f"Movie '{title}' added successfully!")

# Return to View Movies button
if st.button("🔙 Return to View Movies"):
    st.query_params.update(page="View_Movies", role=st.session_state.role)
    st.switch_page("pages/2_View_Movies.py")
