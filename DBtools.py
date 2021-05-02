import pymysql
import time
import subscriber
# import mysql.connector


# getting mysql cursor
def get_dbCursor():
    # create database connection
    dbIP = "127.0.0.1"
    dbUserName = "root"
    dbUserPassword = "reallysecurepwd"

    dbToReset = "patients"
    charSet = "utf8mb4"  # Character set

    cursorType = pymysql.cursors.DictCursor

    # define connection
    connection = pymysql.connect(host=dbIP, user=dbUserName, password=dbUserPassword,
                                 charset=charSet, cursorclass=cursorType)
    # Create a cursor object
    dbCursor = connection.cursor()
    return dbCursor


# restarting mysql database
def restartDB():
    # reset test counts to 0
    subscriber.reset_count()
    try:
        # Get cursor object
        dbCursor = get_dbCursor()

        if resetDB(dbCursor) is True:
            # create the database
            sqlQuery = "CREATE DATABASE patients"
            dbCursor.execte(sqlQuery)
            # create a patient table
            sqlQuery = "CREATE TABLE patient(mrn varchar(255) PRIMARY_KEY, " \
                       "first_name varchar(31), " \
                       "last_name varchar(31), " \
                       "zip_code int, " \
                       "patient_status_code int, " \
                       "hospital_id int"
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
        if database == 'patients':
            reset = False

    return reset


# adding a patient to mysql database
def add_patient(f_name, l_name, mrn, zip_code, status):
    dbCursor = get_dbCursor()
    query = "INSERT INTO patient" \
            " VALUES " + f_name + " " + l_name \
            + zip_code + " " + mrn + " " \
            + status
    dbCursor.execute(query)
