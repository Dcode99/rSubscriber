import pymysql
import time
import pymongo
import json
import subscriber


# import mysql.connector


# getting mysql cursor
def get_dbConnection():
    # create database connection
    dbIP = "127.0.0.1"
    dbUserName = "root"
    dbUserPassword = "reallysecurepwd"

    dbToReset = "patients"
    charSet = "utf8mb4"  # Character set

    cursorType = pymysql.cursors.DictCursor

    # define connection
    connection = pymysql.connect(host=dbIP, user=dbUserName, database="patients", password=dbUserPassword,
                                 charset=charSet, cursorclass=cursorType)
    return connection


# getting mysql cursor
def get_dbCursor():
    connection = get_dbConnection()
    # Create a cursor object
    dbCursor = connection.cursor()
    return dbCursor


def startDB():
    dbCursor = get_dbCursor()

    sqlQuery = "CREATE DATABASE IF NOT EXISTS patients"
    dbCursor.execute(sqlQuery)
    # create a patient table
    sqlQuery = "CREATE TABLE IF NOT EXISTS patient (mrn varchar(255), " \
               "first_name varchar(32), " \
               "last_name varchar(32), " \
               "zip_code int, " \
               "patient_status_code int, " \
               "hospital_id int)"
    dbCursor.execute(sqlQuery)
    get_dbConnection().commit()


# restarting mysql database
def restartDB():
    # reset test counts to 0
    subscriber.reset_count()
    try:

        # Get cursor object
        dbCursor = get_dbCursor()
        resetDB(dbCursor)
        # create the database
        sqlQuery = "CREATE DATABASE patients"
        dbCursor.execute(sqlQuery)
        dbCursor = get_dbCursor()
        # create a patient table
        sqlQuery = "CREATE TABLE patient (mrn varchar(255), " \
                   "first_name varchar(32), " \
                   "last_name varchar(32), " \
                   "zip_code int, " \
                   "patient_status_code int, " \
                   "hospital_id int)"
        dbCursor.execute(sqlQuery)
        get_dbConnection().commit()
        return dbCursor
    except Exception as e:
        print("Exception occurred:{}".format(e))
    try:
        while True:
            time.sleep(5000)
    except Exception as ex:
        print(ex)


# checking if database is reset
def resetDB(dbCursor):
    # function to reset the patient db using mysql
    reset = True
    dbToReset = 'patients'

    # SQL Statement to delete a database
    sql = "DROP DATABASE " + dbToReset

    # Execute the create database SQL statement through the cursor instance
    dbCursor.execute(sql)

    # SQL query string
    sqlQuery = "SHOW DATABASES"

    # Execute the sqlQuery
    dbCursor.execute(sqlQuery)

    # Fetch all the rows
    databaseCollection = dbCursor.fetchall()
    # Check if db exists
    for database in databaseCollection:
        # if the database still exists, it was not reset
        if database['Database'] == "patients":
            reset = False
    return reset


# adding a patient to mysql database
def add_patient(f_name, l_name, mrn, zip_code, status):
    dbCursor = get_dbCursor()
    first_part = "(mrn, first_name, last_name, zip_code, patient_status_code, hospital_id)"
    second_part = "(\"" + mrn + "\", \"" + f_name + "\", \"" + l_name + "\", " + zip_code + ", " + status + ", -1)"
    query = "INSERT INTO patient " + first_part + " VALUES" + second_part
    dbCursor.execute(query)
    get_dbConnection().commit()


def mongo_connect():
    # Getting mongoDB setup
    # TO DO: Add database URL
    database_url = 'cluster0.icc7p.mongodb.net'
    client = pymongo.MongoClient(database_url)

    # Connecting to the database
    mydb = client['hospitaldistances']

    # Connecting the to collection
    # TO DO: add collection name
    collection_name = 'distance'
    col = mydb[collection_name]


def route_patient(zipcode, status):
    # decide which (if any) hospital to send the patient to
    col = pymongo.MongoClient('cluster0.icc7p.mongodb.net')['hospitaldistances']['distance']
    assignment = 0
    # send home
    if status == 1 or status == 2 or status == 3 or status == 4:
        return assignment
    # send to a hospital (if 6, more strict)
    elif status == 3 or status == 5:
        # return closest zipcodes
        doc = col.find().sort("distance", -1)
    elif status == 6:
        # return closest zipcodes
        doc = col.find().sort("distance", -1)
