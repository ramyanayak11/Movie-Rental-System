# Movie-Rental-System


Authors: Ramya Nayak and Thi Dao Nguyen Pham
December 09, 2024



This is the README for our Movie Rental System (Final Project for CS 157A).



For our project, we created a movie rental database system to support a seamless experience for users wanting to rent movies. This system not only efficiently stores information about movies available for rent, but also features a user-friendly interface. Such a system is resourceful to various groups of individuals, including the manager of the movie rental store, the store’s staff members, and its customers.




------------ INSTRUCTIONS FOR SETTING UP AND RUNNING THE PROJECT: -------------

	To set up this project, you need to install the requirements and follow the configuration steps, both of which are described below. Then, using the command line, open the src folder (you can use the following command: cd FinalProject_Code/src). Then, run the 1_Home.py file using Streamlit (this can be done by running the following command: streamlit run 1_Home.py). Running this project successfully should open a local host website showing a home page that asks the user to select their role. Please check the demo in our presentation video to see what the webpage should look like.



--------------------- DEPENDENCIES AND REQUIRED SOFTWARE: ---------------------

	Install Python (version 3.8 or later) - Because our code is written in Python, you would need to have Python installed in order to run it. (can be downloaded from here: https://www.python.org/downloads/)

	Install Streamlit - The front-end of our application uses Streamlit, a Python framework. (can be downloaded from the command line using the following command: pip install streamlit)

	Install HSQLDB - This is the RDBMS our application uses. (can be downloaded from here: https://sourceforge.net/projects/hsqldb/files/)



----------------------- ADDITIONAL CONFIGURATION STEPS: -----------------------

	In order to successfully connect to the database, please download install HSQLDB, as directed above. Then, in our src folder, go to the helper folder and open the function.py file (FinalProject_Code --> src --> helper --> functions.py). Now, replace the value of the hsqldb_jar_path variable with the absolute path to the HSQLDB folder you downloaded. This should allow you to successfully connect to the database and run our program.
