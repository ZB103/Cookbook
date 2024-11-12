# Cookbook
Collaborators: Team Chefs of CSC 403, Fall 2024
Zoe Baker
Bryce Bailey
Will Coker
Connor Ettinger


Start the mySQL server and run cookbook_database_creation.sql in order to load the database. After the server and database are up and running, then you need to run the CookbookHelperFunctions.sql and SqlTriggers.sql for the database to behave exactly as it should. Next to try out Cookbook, you will need flask, downloaded with the following commands:
python -m pip install flask
python -m pip install mysql-connector-python
Next, change the directories, username, and password in the python code main.py to match the database.
Run main.py in a terminal and navigate to the given IP address on a browser of your choice.
python main.py
This will bring you to the sign-in page by default. Once here, you can sign in or create an account. This will then lead you to the home page, where you can see a number of posts recommended to you as well as links to other pages and a button to create your own post.
Happy cooking!
