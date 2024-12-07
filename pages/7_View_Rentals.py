# SHOWS THE RENTALS TABLE
# ALONG WITH JOIN ON MOVIES TO GET MOVIE NAMES

import streamlit as st
import pandas as pd
from helper.functions import fetch_table_data, connect_database  # Import connect_database

# only staff members can view rental records
if "role" not in st.session_state or st.session_state.role != "Staff":
    st.warning("ACCESS DENIED: You must be a Staff member to access this page.")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - View Rentals", page_icon="🎬")  # sets page title and logo (on tab)
st.title("View Rentals")
st.subheader("Rentals")

# Search options
search_option = st.selectbox("Search by", ["Rental ID", "Customer ID", "Movie ID"])
search_input = st.text_input(f"Enter {search_option}")

# Function to search rentals based on the option and input
def search_rentals(option, query):
    conn = connect_database()
    c = conn.cursor()
    
    try:
        if option == "Rental ID":
            query = int(query)  # Convert to integer for Rental ID
            c.execute('''
                SELECT r.RentalID, r.CustomerID, r.MovieID, r.RentalDate, r.ReturnDate, r.TotalPayment
                FROM RentalRecords r
                WHERE r.RentalID = ?
            ''', (query,))
        elif option == "Customer ID":
            query = int(query)  # Convert to integer for Customer ID
            c.execute('''
                SELECT r.RentalID, r.CustomerID, r.MovieID, r.RentalDate, r.ReturnDate, r.TotalPayment
                FROM RentalRecords r
                WHERE r.CustomerID = ?
            ''', (query,))
        elif option == "Movie ID":
            query = int(query)  # Convert to integer for Movie ID
            c.execute('''
                SELECT r.RentalID, r.CustomerID, r.MovieID, r.RentalDate, r.ReturnDate, r.TotalPayment
                FROM RentalRecords r
                WHERE r.MovieID = ?
            ''', (query,))
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
    rentals, columns = search_rentals(search_option, search_input)
else:
    rentals = fetch_table_data("RentalRecords")
    columns = ["RENTALID", "CUSTOMERID", "MOVIEID", "RENTALDATE", "RETURNDATE", "TOTALPAYMENT"]
    if not rentals:  # If no data is returned, show a warning message
        st.warning("No data found in the RentalRecords table.")

# Display the results
if not rentals:
    st.write("No rental records found.")
else:
    # Convert to a DataFrame
    df = pd.DataFrame(rentals, columns=columns)
    
    # Check if df contains all NaN values in each column
    if df.isna().all().all():
        st.warning("The RentalRecords table has no data to display.")
    else:
        st.table(df)  # Display the DataFrame as a table

