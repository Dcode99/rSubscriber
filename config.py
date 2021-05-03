DEBUG = True

#set app directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#Define SQLite database
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'app.db')
DBCONNECT = {}

#Set number of threads
THREADS_PER_PAGE = 2
