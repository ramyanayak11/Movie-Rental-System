# SHOWS THE CUSTOMERS TABLES

import streamlit as st
import pandas as pd
from helper.functions import fetch_table_data, connect_database  # Import connect_database

# Only staff members can view all customers
if "role" not in st.session_state or st.session_state.role != "Staff":
    st.warning("ACCESS DENIED: You must be a Staff member to access this page.")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - View Customers", page_icon="🎬")
st.title("View Customers")
st.subheader("Customers")

# Search options
search_option = st.selectbox("Search by", ["Customer ID", "Name", "Email", "Phone"])
search_input = st.text_input(f"Enter {search_option}")

def search_customers(option, query):
    conn = connect_database()
    c = conn.cursor()
    
    try:
        if option == "Customer ID":
            query = int(query)  # Convert to integer for Customer ID
            c.execute("SELECT * FROM Customers WHERE CustomerID = ?", (query,))
        elif option == "Name":
            c.execute("SELECT * FROM Customers WHERE LOWER(CustomerName) LIKE ?", (f"%{query.lower()}%",))
        elif option == "Email":
            c.execute("SELECT * FROM Customers WHERE LOWER(CustomerEmail) LIKE ?", (f"%{query.lower()}%",))
        elif option == "Phone":
            c.execute("SELECT * FROM Customers WHERE CustomerPhone LIKE ?", (f"%{query}%",))
    except ValueError:
        st.error("Invalid input. Please enter a valid ID number.")
        return [], []  # Return empty lists if error occurs
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return [], []  # Return empty lists if an error occurs
    finally:
        conn.close()

    result = c.fetchall()
    column_names = [description[0] for description in c.description]  # Get column names
    return result, column_names

# Fetch data based on search input
if search_input:
    customers, columns = search_customers(search_option, search_input)
else:
    customers = fetch_table_data("Customers")
    columns = ["CUSTOMERID", "CUSTOMERNAME", "CUSTOMEREMAIL", "CUSTOMERPHONE"]  # Adjusted columns
    if not customers:
        st.warning("No data found in the Customers table.") 

# Display the results
if not customers:
    st.write("No customers found.")
else:
    # Convert to DataFrame
    df = pd.DataFrame(customers, columns=columns)
    # Check if DataFrame contains all NaN values in each column
    if df.isna().all().all():
        st.warning("The Customers table has no data to display.")
    else:
        st.table(df)

