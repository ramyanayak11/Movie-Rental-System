# SHOWS THE STAFF TABLES

import streamlit as st
import pandas as pd
from helper.functions import fetch_table_data, connect_database

# only staff members or administrators can view all staff
if "role" not in st.session_state or (st.session_state.role != "Staff" and st.session_state.role != "Administrator"):
    st.warning("ACCESS DENIED: You must be a Staff member or an Administrator to access this page.")
    st.stop()

# UI details
st.set_page_config(page_title="Movie Rentals - View Staff", page_icon="🎬")
st.title("View Staff")
st.subheader("Staff")

# Search options
search_option = st.selectbox("Search by", ["Staff ID", "Name", "Email", "Phone"])
search_input = st.text_input(f"Enter {search_option}")


def search_staff(option, query):
    conn = connect_database()
    c = conn.cursor()

    try:
        if option == "Staff ID":
            query = int(query)  # Convert to integer for Customer ID
            c.execute("SELECT * FROM Staff WHERE StaffID = ?", (query,))
        elif option == "Name":
            c.execute("SELECT * FROM Staff WHERE LOWER(StaffName) LIKE ?", (f"%{query.lower()}%",))
        elif option == "Email":
            c.execute("SELECT * FROM Staff WHERE LOWER(StaffEmail) LIKE ?", (f"%{query.lower()}%",))
        elif option == "Phone":
            c.execute("SELECT * FROM Staff WHERE StaffPhone LIKE ?", (f"%{query}%",))
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
    staff, columns = search_staff(search_option, search_input)
else:
    staff = fetch_table_data("Staff")
    columns = ["STAFFID", "STAFFNAME", "STAFFEMAIL", "STAFFPHONE", "STARTDATE"]  # Adjusted columns
    if not staff:
        st.warning("No data found in the Staff table.")

    # Display the results
if not staff:
    st.write("No staff found.")
else:
    # Convert to DataFrame
    df = pd.DataFrame(staff, columns=columns)
    # Check if DataFrame contains all NaN values in each column
    if df.isna().all().all():
        st.warning("The Staff table has no data to display.")
    else:
        st.table(df)