# SHOWS THE RATINGS TABLE
# ALONG WITH JOIN ON MOVIES TO GET MOVIE NAMES

import streamlit as st
import pandas as pd
from helper.functions import fetch_table_data, connect_database, create_menu  # Import connect_database

# UI details
st.set_page_config(page_title="Movie Rentals - View Reviews", page_icon="🎬",  layout="wide", initial_sidebar_state="collapsed")   # sets page title and logo (on tab)
create_menu()
st.title("View Reviews")
st.subheader("Reviews")

# Buttons for navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add Review"):
        st.query_params.update(page="Add_Reviews", role=st.session_state.role)
        st.switch_page("pages/11_Add_Reviews.py")
with col2:
    if st.button("🗑️ Delete Review"):
        st.query_params.update(page="Delete_Review", role=st.session_state.role)
        st.switch_page("pages/12_Delete_Review.py")

# Search options
search_option = st.selectbox("Search by", ["Rating ID", "Customer ID", "Movie ID","Movie Title", "Rating Score"])
search_input = st.text_input(f"Enter {search_option}")

# Function to search reviews based on the option and input
def search_reviews(option, query):
    conn = connect_database()
    c = conn.cursor()
    
    try:
        if option == "Rating ID":
            query = int(query)  # Convert to integer for Rating ID
            c.execute('''
                SELECT r.RatingID, r.CustomerID, r.MovieID, m.MovieTitle,
                       r.RatingScore, r.Review, r.RatingDate
                FROM Ratings r
                LEFT JOIN Movies m ON r.MovieID = m.MovieID
                WHERE r.RatingID LIKE ?
            ''', (f"{query}%",))
        elif option == "Customer ID":
            query = int(query)  # Convert to integer for Customer ID
            c.execute('''
                SELECT r.RatingID, r.CustomerID, r.MovieID, m.MovieTitle,
                       r.RatingScore, r.Review, r.RatingDate
                FROM Ratings r
                LEFT JOIN Movies m ON r.MovieID = m.MovieID
                WHERE r.CustomerID LIKE ?
            ''', (f"{query}%",))
        elif option == "Movie ID":
            query = int(query)  # Convert to integer for Movie ID
            c.execute('''
                SELECT r.RatingID, r.CustomerID, r.MovieID, m.MovieTitle,
                       r.RatingScore, r.Review, r.RatingDate
                FROM Ratings r
                LEFT JOIN Movies m ON r.MovieID = m.MovieID
                WHERE r.MovieID LIKE ?
            ''', (f"{query}%",))
        elif option == "Movie Title":
            query = query.lower()
            c.execute('''
                SELECT r.RatingID, r.CustomerID, r.MovieID, m.MovieTitle,
                       r.RatingScore, r.Review, r.RatingDate
                FROM Ratings r
                LEFT JOIN Movies m ON r.MovieID = m.MovieID
                WHERE LOWER(m.MovieTitle) LIKE ?
            ''', (f"%{query}%",))
        elif option == "Rating Score":
            query = float(query)  # Convert to float for Rating Score
            c.execute('''
                SELECT r.RatingID, r.CustomerID, r.MovieID, m.MovieTitle,
                       r.RatingScore, r.Review, r.RatingDate
                FROM Ratings r
                LEFT JOIN Movies m ON r.MovieID = m.MovieID
                WHERE r.RatingScore = ?
            ''', (query,))
    except ValueError:
        st.error("Invalid input. Please enter a valid number.")
        return [], []  # Return empty lists for both result and columns in case of error
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return [], []  # Return empty lists for both result and columns in case of error
    finally:
        conn.close()
    
    result = c.fetchall()
    column_names = [description[0] for description in c.description]  # Get column names
    
    # Replace None or empty values in MovieTitle with 'No Movie Title'
    for i in range(len(result)):
        if result[i][6] is None or result[i][6] == '':  # Check if MovieTitle is None or empty
            result[i] = result[i][:6] + ('No Movie Title',)  # Add 'No Movie Title' in the MovieTitle column
    return result, column_names

# Fetch data based on search input
if search_input:
    reviews, columns = search_reviews(search_option, search_input)
else:
    reviews = fetch_table_data("Ratings")
    columns = ["RATINGID", "CUSTOMERID", "MOVIEID", "MOVIETITLE", "RATINGSCORE", "REVIEW", "RATINGDATE"]
    if not reviews:  # If no data is returned, show a warning message
        st.warning("No data found in the Ratings table.")

# Display the results
if not reviews:
    st.write("No reviews found.")
else:
    # Convert to a DataFrame
    df = pd.DataFrame(reviews, columns=columns)
    
    # Check if df contains all NaN values in each column
    if df.isna().all().all():
        st.warning("The Ratings table has no data to display.")
    else:
        st.table(df)  # Display the DataFrame as a table
