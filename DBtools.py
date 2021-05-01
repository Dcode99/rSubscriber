import pymysql
import mysql.connector


def startDB():
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

        if resetDB() is True:
            sqlQuery = "CREATE DATABASE patients"
            dbCursor.execte(sqlQuery)
            sqlQuery = "CREATE TABLE patient(mrn varchar(255) PRIMARY_KEY, " \
                       "first_name varchar(31), " \
                       "last_name varchar(31), " \
                       "zip_code int, " \
                       "patient_status_code int, " \
                       "hospital_id int"

    except Exception as e:
        print("Exception occurred:{}".format(e))


def resetDB():
    # function to reset the patient db using mysql
    reset = True

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
        if database == 'patients':
            reset = False

    return reset
