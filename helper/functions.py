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
        FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
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
        FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    );
    ''')

    conn.commit()
    conn.close()


# add sample data to all tables
def add_sample_data():
    conn = connect_database()
    c = conn.cursor()

    # check if tables are empty, and only add sample data if they're empty
    c.execute("SELECT COUNT(*) FROM Movies")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Movies (MovieID, MovieTitle, ReleaseDate, Genre, Length, RentalRate) VALUES"
            "(1, 'The Shawshank Redemption', '1994-09-22', 'Drama', 142, 3.99), "
            "(2, 'The Godfather', '1972-03-24', 'Crime', 175, 4.50), "
            "(3, 'The Dark Knight', '2008-07-18', 'Action', 152, 3.99), "
            "(4, 'Pulp Fiction', '1994-10-14', 'Crime', 154, 4.25), "
            "(5, 'Inception', '2010-07-16', 'Sci-Fi', 148, 3.50);")

    c.execute("SELECT COUNT(*) FROM Customers")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Customers (CustomerID, CustomerName, CustomerEmail, CustomerPhone) VALUES"
            "(1, 'Alice Johnson', 'alice.johnson@example.com', '123-456-7890'), "
            "(2, 'Bob Smith', 'bob.smith@example.com', '234-567-8901'), "
            "(3, 'Charlie Brown', 'charlie.brown@example.com', '345-678-9012'), "
            "(4, 'Diana Prince', 'diana.prince@example.com', '456-789-0123'), "
            "(5, 'Evan Rogers', 'evan.rogers@example.com', '567-890-1234');")

    c.execute("SELECT COUNT(*) FROM Staff")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Staff (StaffID, StaffName, StaffEmail, StaffPhone, StartDate) VALUES"
            "(1, 'Emily Davis', 'emily.davis@example.com', '987-654-3210', '2020-06-01'), "
            "(2, 'John Carter', 'john.carter@example.com', '876-543-2109', '2021-04-15'), "
            "(3, 'Sarah Lee', 'sarah.lee@example.com', '765-432-1098', '2019-11-20');")

    c.execute("SELECT COUNT(*) FROM RentalRecords")
    count = c.fetchone()[0]
    if count == 0:
        c.execute(
            "INSERT INTO RentalRecords (RentalID, MovieID, CustomerID, RentalRate, RentalDate, ReturnDeadline, ReturnDate, LateFee, TotalPayment) VALUES"
            "(1, 1, 2, 3.99, '2024-11-19', '2024-11-26', '2024-11-26', 0.00, 3.99), "
            "(2, 3, 4, 3.99, '2024-11-20', '2024-11-27','2024-11-29', 1.00, 4.99), "
            "(3, 2, 1, 4.50, '2024-11-22', '2024-11-29', '2024-11-30', 0.50, 5.00), "
            "(4, 4, 3, 3.50, '2024-11-23', '2024-11-30', NULL, NULL, NULL);")

    c.execute("SELECT COUNT(*) FROM Ratings")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Ratings (RatingID, MovieID, CustomerID, RatingScore, Review, RatingDate) VALUES"
            "(1, 1, 2, 10, 'Absolutely loved it. A timeless classic.', '2024-11-26'), "
            "(2, 2, 1, 9, 'A masterpiece in storytelling.', '2024-11-24'), "
            "(3, 3, 4, 8, 'Great action sequences but a bit too long.', '2024-11-25'), "
            "(4, 3, 4, 7, 'Unique but not my favorite.', '2024-11-27');")

    conn.commit()
    conn.close()

# get all data from specified table
def fetch_table_data(table_name, fromRentals=False, fromRatings=False):
    conn = connect_database()
    c = conn.cursor()

    # uses JOIN to get movie title if data is fetched from View Rentals or View Reviews page
    if fromRentals:
        c.execute('''
                SELECT RentalRecords.RentalID, RentalRecords.MovieID, Movies.MovieTitle, RentalRecords.RentalRate, RentalRecords.RentalDate, RentalRecords.ReturnDeadline, RentalRecords.ReturnDate, RentalRecords.LateFee, RentalRecords.TotalPayment
                FROM RentalRecords
                JOIN Movies ON RentalRecords.MovieID = Movies.MovieID
            ''')
    elif fromRatings:  # uses JOIN to get movie title if data is fetched from View Reviews page
        c.execute('''
                SELECT Movies.MovieTitle, Ratings.RatingScore, Ratings.Review, Ratings.RatingDate, Ratings.CustomerID
                FROM Ratings
                JOIN Movies ON Ratings.MovieID = Movies.MovieID
            ''')
    else:           # otherwise just get data from the original table
        c.execute(f"SELECT * FROM {table_name}")

    columns = [description[0] for description in c.description] # get column names
    rows = c.fetchall()

    results = [dict(zip(columns, row)) for row in rows]         # convert to dictionary

    conn.close()

    return results
