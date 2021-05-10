import pandas as pd
import pymysql


# import mysql.connector
# getting mysql cursor
def get_db_hospital_connection():
    # create database connection
    dbIP = "127.0.0.1"
    dbUserName = "root"
    dbUserPassword = "reallysecurepwd"

    db = "rhospitalpatients"
    charSet = "utf8mb4"  # Character set

    cursorType = pymysql.cursors.DictCursor

    # define connection
    connection = pymysql.connect(host=dbIP, user=dbUserName, database=db, password=dbUserPassword,
                                 charset=charSet, cursorclass=cursorType, autocommit=True)
    return connection


# getting mysql cursor
def get_db_hospital_cursor():
    connection = get_db_hospital_connection()
    # Create a cursor object
    dbCursor = connection.cursor()
    return dbCursor


# one-time function to get hospital data from CSV
def read_hospitals():
    # read data from CSV path
    data = pd.read_csv(r'E:\download\hospitals.csv', index_col=None)
    # print(data['ID'])
    # parse data into columns needed
    df = pd.DataFrame(data, columns=['ID', 'BEDS', 'ZIP', 'TRAUMA'])
    for i, row in df.iterrows():
        query1 = 'INSERT INTO hospitals VALUES (\'' + str(row['ID']) + '\',' + str(row['BEDS']) + ','
        query2 = str(row['ZIP']) + ',\'' + str(row['TRAUMA']) + '\')'
        # print(row)
        get_db_hospital_cursor().execute(query1 + query2)
    return df


# one-time function to get zip_code data from CSV
def read_distance():
    # read data from CSV path
    data = pd.read_csv(r'E:\download\kyzipdistance.csv')
    # parse data into columns needed
    df = pd.DataFrame(data, columns=['zip_to', 'zip_from', 'distance'])
    return df


class Distances:
    def __init__(self):
        self.df = read_distance()

    # set new datafile
    def setdf(self):
        df = self

    # return datafile
    def getdf(self):
        return self.df
