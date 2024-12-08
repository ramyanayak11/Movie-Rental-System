# CONTAINS HELPER FUNCTIONS
# CALLED FROM MULTIPLE PAGES

import jaydebeapi as jdbc

# database connection function
# note: the connect_database() method gives an error when absolute paths aren't used
hsqldb_jar_path = "/Users/nguyenpham/Downloads/apps/hsqldb-2.7.4/hsqldb/lib/hsqldb.jar"  # for connecting to db
def connect_database():
    conn = jdbc.connect("org.hsqldb.jdbcDriver","jdbc:hsqldb:mem:movierentaldb",
                        {'user': "SA", 'password': ""}, hsqldb_jar_path)
    return conn

# create tables function for all tables
def create_tables():
    conn = connect_database()
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS Movies (
        MovieID INTEGER PRIMARY KEY,
        MovieTitle VARCHAR(255) NOT NULL,
        ReleaseDate DATE NOT NULL,
        Genre VARCHAR(100) NOT NULL,
        Length INTEGER NOT NULL,
        RentalRate DECIMAL(5, 2) NOT NULL
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY,
        CustomerName VARCHAR(255) NOT NULL,
        CustomerEmail VARCHAR(255) UNIQUE NOT NULL,
        CustomerPhone VARCHAR(20) NOT NULL
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Staff (
        StaffID INTEGER PRIMARY KEY,
        StaffName VARCHAR(255) NOT NULL,
        StaffEmail VARCHAR(255) UNIQUE NOT NULL,
        StaffPhone VARCHAR(20) NOT NULL,
        StartDate DATE NOT NULL
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS RentalRecords (
        RentalID INTEGER PRIMARY KEY,
        MovieID INTEGER NOT NULL,
        CustomerID INTEGER NOT NULL,
        RentalRate DECIMAL(5, 2) NOT NULL,
        RentalDate DATE NOT NULL,
        ReturnDeadline DATE NOT NULL,
        ReturnDate DATE,
        LateFee DECIMAL(5, 2),
        TotalPayment DECIMAL(5, 2),
        FOREIGN KEY (MovieID) REFERENCES Movies(MovieID) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Ratings (
        RatingID INTEGER PRIMARY KEY,
        MovieID INTEGER NOT NULL,
        CustomerID INTEGER NOT NULL,
        RatingScore INTEGER CHECK (RatingScore BETWEEN 1 AND 10),
        Review VARCHAR(1000),
        RatingDate DATE NOT NULL,
        FOREIGN KEY (MovieID) REFERENCES Movies(MovieID) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    );
    ''')

    conn.commit()
    conn.close()


# add sample data to all tables
def add_sample_data():
    conn = connect_database()
    c = conn.cursor()

    # only add sample data if the tables are empty
    c.execute("SELECT COUNT(*) FROM Movies")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Movies (MovieID, MovieTitle, ReleaseDate, Genre, Length, RentalRate) VALUES"
                    "(1, 'Charlie & the Chocolate Factory', '2005-07-10', 'Family/Fantasy', 115, 3.99), "
                    "(2, 'The Hunger Games', '2012-03-23', 'Action/Adventure', 142, 4.50), "
                    "(3, 'Now You See Me', '2013-05-31', 'Thriller/Crime', 115, 3.99), "
                    "(4, 'Jumanji: Welcome to the Jungle', '2017-12-20', 'Adventure/Action', 119, 3.50), "
                    "(5, 'Moana', '2016-11-23', 'Family/Adventure', 103, 2.99), "
                    "(6, 'The Godfather', '1972-03-24', 'Crime', 175, 1.99), "
                    "(7, 'The Dark Knight', '2008-07-18', 'Action/Crime', 152, 2.99), "
                    "(8, 'Pulp Fiction', '1994-10-14', 'Crime/Thriller', 149, 1.99), "
                    "(9, 'Frozen 2', '2019-11-22', 'Family/Fantasy', 103, 2.99), "
                    "(10, 'The Martian', '2015-10-02', 'Sci-Fi/Adventure', 151, 3.99), "
                    "(11, 'Titanic', '1997-12-19', 'Romance/Adventure', 195, 4.50), "
                    "(12, 'Truth or Dare', '2018-04-13', 'Horror/Action', 110, 2.99), "
                    "(13, 'The Shawshank Redemption', '1994-10-14', 'Thriller/Crime', 142, 2.99), "
                    "(14, 'Subservience', '2024-08-15', 'Thriller/Sci-Fi', 111, 4.50), "
                    "(15, 'Dune', '2021-10-22', 'Sci-Fi/Adventure', 155, 3.99), "
                    "(16, 'Inception', '2010-07-13', 'Action/Sci-Fi', 148, 2.99);")

    c.execute("SELECT COUNT(*) FROM Customers")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Customers (CustomerID, CustomerName, CustomerEmail, CustomerPhone) VALUES"
                    "(1, 'Liam Johnson', 'liam.johnson@example.com', '123-456-7890'), "
                    "(2, 'Sarah Smith', 'sarah.smith@example.com', '234-567-8901'), "
                    "(3, 'Noah Brown', 'noah.brown@example.com', '345-678-9012'), "
                    "(4, 'Amelia Jones', 'amelia.jones@example.com', '456-789-0123'), "
                    "(5, 'Oliver Wang', 'oliver.wang@example.com', '123-452-7890'), "
                    "(6, 'Diana Hertz', 'diana.hertz@example.com', '284-567-8901'), "
                    "(7, 'James Miller', 'james.miller@example.com', '395-678-9012'), "
                    "(8, 'Emma Price', 'emma.price@example.com', '450-789-0123'), "
                    "(9, 'Charles Jackson', 'charles.jackson@example.com', '519-890-1234'), "
                    "(10, 'Isabella Martin', 'isabella.martin@example.com', '121-456-7890'), "
                    "(11, 'Michael Scott', 'michael.scott@example.com', '234-767-8901'), "
                    "(12, 'Jennifer Anderson', 'jennifer.anderson@example.com', '305-678-9012'), "
                    "(13, 'David Lee', 'david.lee@example.com', '456-780-0123'), "
                    "(14, 'Olivia White', 'olivia.white@example.com', '527-890-1234'), "
                    "(15, 'Evan Brown', 'evan.brown@example.com', '547-890-1294'), "
                    "(16, 'Sophia Garcia', 'sophia.garcia@example.com', '597-893-1224');")

    c.execute("SELECT COUNT(*) FROM Staff")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Staff (StaffID, StaffName, StaffEmail, StaffPhone, StartDate) VALUES"
                  "(1, 'Carol Brown', 'carol.brown@example.com', '516-549-2819', '2010-01-15'), "
                  "(2, 'Sarah Lee', 'sarah.lee@example.com', '765-432-1098', '2011-06-20'), "
                  "(3, 'Leah Smith', 'leah.smith@example.com', '928-644-3990', '2012-02-29'), "
                  "(4, 'Emily Davis', 'emily.davis@example.com', '987-654-3210', '2013-04-01'), "
                  "(5, 'John Carter', 'john.carter@example.com', '876-543-2109', '2014-09-10'), "
                  "(6, 'Michael Brown', 'michael.brown@example.com', '321-654-9870', '2015-03-05'), "
                  "(7, 'Sophia Wilson', 'sophia.wilson@example.com', '432-987-1234', '2016-07-12'), "
                  "(8, 'David Johnson', 'david.johnson@example.com', '543-210-6789', '2017-01-18'), "
                  "(9, 'Olivia Martin', 'olivia.martin@example.com', '654-321-9876', '2018-08-03'), "
                  "(10, 'Liam Scott', 'liam.scott@example.com', '765-432-1987', '2019-10-25'), "
                  "(11, 'Emma Wright', 'emma.wright@example.com', '876-543-2198', '2020-03-15'), "
                  "(12, 'Daniel Lee', 'daniel.lee@example.com', '987-654-3120', '2020-09-30'), "
                  "(13, 'Ava Green', 'ava.green@example.com', '213-456-7890', '2021-05-06'), "
                  "(14, 'Lucas White', 'lucas.white@example.com', '324-567-8901', '2022-02-14'), "
                  "(15, 'Isabella King', 'isabella.king@example.com', '435-678-9012', '2023-01-22'), "
                  "(16, 'James Hall', 'james.hall@example.com', '546-789-0123', '2023-07-11');")

    c.execute("SELECT COUNT(*) FROM RentalRecords")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO RentalRecords (RentalID, MovieID, CustomerID, RentalRate, RentalDate, "
                  "ReturnDeadline, ReturnDate, LateFee, TotalPayment) VALUES"
                    "(1, 1, 2, 3.99, '2024-11-19', '2024-11-26', '2024-11-26', 0.00, 3.99), "
                    "(2, 3, 4, 3.99, '2024-11-20', '2024-11-27', '2024-11-29', 1.00, 4.99), "
                    "(3, 2, 1, 4.50, '2024-11-22', '2024-11-29', '2024-11-30', 0.50, 5.00), "
                    "(4, 4, 3, 3.50, '2024-11-23', '2024-11-30', '2024-12-01', 0.50, 4.00), "
                    "(5, 5, 6, 2.99, '2024-11-24', '2024-12-01', '2024-12-01', 0.00, 2.99), "
                    "(6, 6, 5, 1.99, '2024-11-25', '2024-12-02', '2024-12-03', 0.50, 2.49), "
                    "(7, 7, 8, 2.99, '2024-11-26', '2024-12-03', '2024-12-04', 0.50, 3.49), "
                    "(8, 8, 7, 1.99, '2024-11-27', '2024-12-04', '2024-12-05', 0.50, 2.49), "
                    "(9, 9, 10, 2.99, '2024-11-28', '2024-12-05', '2024-12-06', 0.50, 3.49), "
                    "(10, 10, 9, 3.99, '2024-11-29', '2024-12-06', '2024-12-06', 0.00, 3.99), "
                    "(11, 11, 12, 4.50, '2024-11-30', '2024-12-07', '2024-12-08', 0.50, 5.00), "
                    "(12, 12, 11, 2.99, '2024-12-01', '2024-12-08', '2024-12-09', 0.50, 3.49), "
                    "(13, 13, 14, 2.99, '2024-12-02', '2024-12-09', '2024-12-09', 0.00, 2.99), "
                    "(14, 14, 13, 4.50, '2024-12-03', '2024-12-10', '2024-12-12', 1.00, 5.50), "
                    "(15, 15, 16, 3.99, '2024-12-04', '2024-12-11', '2024-12-12', 0.50, 4.49), "
                    "(16, 16, 15, 2.99, '2024-12-05', '2024-12-12', '2024-12-13', 0.50, 3.49);")

    c.execute("SELECT COUNT(*) FROM Ratings")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Ratings (RatingID, MovieID, CustomerID, RatingScore, Review, RatingDate) VALUES"
                    "(1, 1, 2, 10, 'Absolutely loved it. A timeless classic.', '2024-11-26'), "
                    "(2, 2, 1, 9, 'A masterpiece in storytelling.', '2024-11-24'), "
                    "(3, 3, 4, 8, 'Great action sequences but a bit too long.', '2024-11-25'), "
                    "(4, 4, 3, 7, 'Unique but not my favorite.', '2024-11-27'), "
                    "(5, 5, 6, 9, 'Visually stunning and emotionally engaging.', '2024-11-22'), "
                    "(6, 6, 7, 8, 'Good but a bit predictable.', '2024-11-21'), "
                    "(7, 7, 8, 10, 'An absolute joy from start to finish.', '2024-11-20'), "
                    "(8, 8, 9, 6, 'Somewhat entertaining but forgettable.', '2024-11-19'), "
                    "(9, 9, 10, 8, 'Fantastic performances and direction.', '2024-11-18'), "
                    "(10, 10, 11, 7, 'Good overall, but the ending fell flat.', '2024-11-23'), "
                    "(11, 11, 12, 10, 'Hilarious and heartwarming!', '2024-11-26'), "
                    "(12, 12, 13, 9, 'A deep and thought-provoking experience.', '2024-11-24'), "
                    "(13, 13, 14, 8, 'A great ride but not for everyone.', '2024-11-25'), "
                    "(14, 14, 15, 7, 'A bit slow, but the payoff was worth it.', '2024-11-27'), "
                    "(15, 15, 16, 9, 'One of the best performances I have seen.', '2024-11-22'), "
                    "(16, 16, 1, 10, 'Perfection! A must-watch.', '2024-11-21');")

    conn.commit()
    conn.close()

# get all data from specified table
def fetch_table_data(table_name):
    conn = connect_database()
    c = conn.cursor()

    # uses JOIN to get movie title if data is fetched from View Rentals or View Reviews page
    if table_name == "RentalRecords":
        c.execute('''
                SELECT RentalRecords.RentalID, RentalRecords.CustomerID, RentalRecords.MovieID, Movies.MovieTitle, RentalRecords.RentalRate, RentalRecords.RentalDate, RentalRecords.ReturnDeadline, RentalRecords.ReturnDate, RentalRecords.LateFee, RentalRecords.TotalPayment
                FROM RentalRecords JOIN Movies
                ON RentalRecords.MovieID = Movies.MovieID
            ''')
    elif table_name == "Ratings":
        c.execute('''
                SELECT Ratings.RatingID, Ratings.CustomerID, Movies.MovieID, Movies.MovieTitle, Ratings.RatingScore, Ratings.Review, Ratings.RatingDate
                FROM Ratings JOIN Movies
                ON Ratings.MovieID = Movies.MovieID
            ''')
    else:           # otherwise just get data from the original table
        c.execute(f"SELECT * FROM {table_name}")

    columns = [description[0] for description in c.description] # get column names
    rows = c.fetchall()

    results = [dict(zip(columns, row)) for row in rows]         # convert to dictionary

    conn.close()

    return results

# --- for the following functions, ensure when calling them that the attribute exists in the given table ---

# validate id exists in a table
def validate_id(table_name, attribute_name, id):
    try:
        conn = connect_database()
        c = conn.cursor()

        # check if the attribute exists
        c.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {attribute_name}={id}")
        exists = c.fetchone()[0] > 0

        conn.close()
        return exists
    except Exception as e:
        st.error(f"Error validating ID ({attribute_name} = {id}): {e}")
        return False

# deletes row from table where the id is a match
def delete_row(table_name, attribute_name, id):
    try:
        conn = connect_database()
        c = conn.cursor()

        # delete row in the table
        c.execute(f"DELETE FROM {table_name} WHERE {attribute_name}={id}")

        conn.close()
    except Exception as e:
        st.error(f"Error deleting row ({attribute_name} = {id}): {e}")
