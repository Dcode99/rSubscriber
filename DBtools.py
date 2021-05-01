import pymysql
import time
import subscriber
# import mysql.connector


def restartDB():
    # reset test counts to 0
    subscriber.reset_count()

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
    try:
        # Create a cursor object
        dbCursor = connection.cursor()

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
