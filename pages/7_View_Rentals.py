# SHOWS THE RENTALS TABLE
# ALONG WITH JOIN ON MOVIES TO GET MOVIE NAMES

import streamlit as st
import pandas as pd
from helper.functions import fetch_table_data, connect_database, create_menu  # Import connect_database

# only staff members or administrators can view rental records
if "role" not in st.session_state or (st.session_state.role != "Staff" and st.session_state.role != "Administrator"):
    st.warning("ACCESS DENIED: You must be a Staff member or an Administrator to access this page.")
    if st.button("Go back to Home"):
        st.switch_page("1_Home.py")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - View Rentals", page_icon="🎬",  layout="wide", initial_sidebar_state="collapsed")  # sets page title and logo (on tab)
create_menu()
st.title("View Rentals")
st.subheader("Rentals")

# Buttons for navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add Rental"):
        st.query_params.update(page="Add_Rental", role=st.session_state.role)
        st.switch_page("pages/8_Add_Rental.py")
with col2:
    if st.button("⏎ Return Rental"):
        st.query_params.update(page="Return_Rental", role=st.session_state.role)
        st.switch_page("pages/9_Return_Rental.py")


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
                SELECT r.RentalID, r.CustomerID, r.MovieID, r.RentalRate, r.RentalDate, r.ReturnDeadline, r.ReturnDate, r.LateFee, r.TotalPayment
                FROM RentalRecords r
                WHERE r.RentalID LIKE ?
            ''', (f"{query}%",))
        elif option == "Customer ID":
            query = int(query)  # Convert to integer for Customer ID
            c.execute('''
                SELECT r.RentalID, r.CustomerID, r.MovieID, r.RentalRate, r.RentalDate, r.ReturnDeadline, r.ReturnDate, r.LateFee, r.TotalPayment
                FROM RentalRecords r
                WHERE r.CustomerID LIKE ?
            ''', (f"{query}%",))
        elif option == "Movie ID":
            query = int(query)  # Convert to integer for Movie ID
            c.execute('''
                SELECT r.RentalID, r.CustomerID, r.MovieID, r.RentalRate, r.RentalDate, r.ReturnDeadline, r.ReturnDate, r.LateFee, r.TotalPayment
                FROM RentalRecords r
                WHERE r.MovieID LIKE ?
            ''', (f"{query}%",))
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
    columns = ["RENTALID", "CUSTOMERID", "MOVIEID", "RENTALRATE", "RENTALDATE", "RETURNDEADLINE", "RETURNDATE",
               "LATEFEE", "TOTALPAYMENT"]
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

