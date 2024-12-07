# SHOWS THE MOVIES TABLES

import streamlit as st
import pandas as pd
from helper.functions import fetch_table_data, connect_database  # Import connect_database

# UI details
st.set_page_config(page_title="Movie Rentals - View Movies", page_icon="🎬")
st.title("View Movies")
st.subheader("Movies")

# Search options
search_option = st.selectbox("Search by", ["Movie ID", "Title", "Genre"])
search_input = st.text_input(f"Enter {search_option}")

def search_movies(option, query):
    conn = connect_database()
    c = conn.cursor()
    
    try:
        if option == "Movie ID":
            query = int(query)  # Convert to integer for Movie ID
            c.execute("SELECT * FROM Movies WHERE MovieID = ?", (query,))
        elif option == "Title":
            c.execute("SELECT * FROM Movies WHERE LOWER(MovieTitle) LIKE ?", (f"%{query.lower()}%",))
        elif option == "Genre":
            c.execute("SELECT * FROM Movies WHERE LOWER(Genre) LIKE ?", (f"%{query.lower()}%",))
    except ValueError:
        st.error("Invalid input. Please enter a valid ID number.")
        return [], []  # Return empty lists for both result and columns in case of error
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return [], []  # Return empty lists for both result and columns in case of error
    finally:
        conn.close()
    
    result = c.fetchall()
    column_names = [description[0] for description in c.description]  # Get column names
    return result, column_names

# Fetch data based on search input
if search_input:
    movies, columns = search_movies(search_option, search_input)
else:
    movies = fetch_table_data("Movies")
    columns = ["MOVIEID", "MOVIETITLE", "RELEASEDATE", "GENRE", "LENGTH", "RENTALRATE"]
    if not movies:  # If no data is returned, show a warning message
        st.warning("No data found in the Movies table.")

# Display the results
if not movies:
    st.write("No movies found.")
else:
    # Convert to a df
    df = pd.DataFrame(movies, columns=columns)
    
    # Check if df contains all NaN values in each column
    if df.isna().all().all():
        st.warning("The Movies table has no data to display.")
    else:
        st.table(df)  # Display the DataFrame as a table

