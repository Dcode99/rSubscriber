import pymysql
import time


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


def startHospitalDB():
    # start mysql hospital database
    db_hospitalConn = get_db_hospital_connection()
    dbCursor = get_db_hospital_cursor()
    get_db_hospital_connection().ping(reconnect=True)

    sqlQuery = "CREATE DATABASE IF NOT EXISTS rhospitalpatients"
    dbCursor.execute(sqlQuery)
    # create a current_capacity column if needed
    # sqlQuery = "ALTER TABLE hospitals ADD COLUMN current_capacity int"
    # dbCursor.execute(sqlQuery)
    db_hospitalConn.commit()


# reset current capacity of all hospitals
def reset_hospital_db():
    dbHospitalConn = get_db_hospital_connection()
    # dbHospitalCursor = get_db_hospital_cursor()
    dbHospitalConn.ping(reconnect=True)
    # sql_delete = "UPDATE hospitals SET current_capacity = 0 WHERE current_capacity is NULL"
    # sql_delete = "ISNULL(current_capacity, 0) FROM hospitals"
    # dbHospitalCursor.execute(sql_delete)
    # dbHospitalConn.commit()


# getting mysql connection
def get_dbConnection():
    # create database connection
    dbIP = "127.0.0.1"
    dbUserName = "root"
    dbUserPassword = "reallysecurepwd"

    db = "patients"
    charSet = "utf8mb4"  # Character set

    cursorType = pymysql.cursors.DictCursor

    # define connection
    connection = pymysql.connect(host=dbIP, user=dbUserName, database=db, password=dbUserPassword,
                                 charset=charSet, cursorclass=cursorType, autocommit=True)
    return connection


# getting mysql cursor
def get_dbCursor():
    connection = get_dbConnection()
    # Create a cursor object
    dbCursor = connection.cursor()
    return dbCursor


def startDB():
    dbCursor = get_dbCursor()
    dbConn = get_dbConnection()
    dbConn.ping(reconnect=True)

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
    dbConn.commit()


# restarting mysql database
def restartDB():
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
    second_part = "(\'" + mrn + "\', \'" + f_name + "\', \'" + l_name + "\', " + zip_code + ", " + status + ", -1)"
    query = "INSERT INTO patient " + first_part + " VALUES " + second_part
    dbCursor.execute(query)
    # get_dbConnection().commit()
    # test lines
    # query = 'SELECT * from patient'
    # return_info = run_query(query)
    # print(return_info)


# deleted mongo module
# def mongo_connect():
#    # Getting mongoDB setup
#    database_url = 'mongodb://deta224:reallysecurepwd@cluster0.icc7p.mongodb.net/'
#    client = pymongo.MongoClient(database_url)
#
#    # Connecting to the database
#    mydb = client['hospitaldistances']
#
#    # Connecting the to collection
#    # TO DO: add collection name
#    collection_name = 'distance'
#    col = mydb[collection_name]

# use patient assignment to assign them in mysql
def insert_assignment(f_name, l_name, assignment):
    dbConn = get_dbConnection()
    dbCursor = get_dbCursor()
    query_p1 = 'INSERT INTO patient (first_name, last_name, hospital_id) values'
    query_p2 = ' (\'' + f_name + '\',\'' + l_name + '\',\'' + str(assignment) + '\')'
    dbCursor.execute(query_p1 + query_p2)
    # dbConn.commit()
    # test lines
    # query = 'SELECT * from patient'
    # return_info = run_query(query)
    # print(return_info)


# create file for hospital capacities
def create_capacities():
    db_hospital_cursor = get_db_hospital_cursor()
    db_hospital_cursor.execute('SELECT ï»¿ID from hospitals')
    results = db_hospital_cursor.fetchall()
    f = open("hospitals.txt", "w")
    for row in results:
        f.writelines(str(row['ï»¿ID']) + ' 0 \n')
    f.close()


# check if capacity is open
def increment_capacity(hospital_id):
    return_info = -1
    f = open("hospitals.txt", "r")
    Lines = f.readlines()
    count = 0
    for line in Lines:
        s_list = line.split(' ')
        if str(hospital_id) == str(s_list[0]):
            return_info = int(s_list[1])
            Lines[count] = str(s_list[0]) + ' ' + str(return_info + 1) + ' \n'
        count = count + 1
    f = open("hospitals.txt", "w")
    f.writelines(Lines)
    f.close()
    # Test print
    # print(str(hospital_id) + " should be " + str(return_info+1))
    return return_info


# check if capacity is open
def check_capacity(hospital_id):
    f = open("hospitals.txt", "r")
    Lines = f.readlines()
    for line in Lines:
        s_list = line.split(' ')
        if hospital_id == s_list[0]:
            return int(s_list[1])
    return 0


def route_patient(zipcode, status, dataframe):
    # decide which (if any) hospital to send the patient to
    assignment = -1
    # send home
    if status == "1" or status == "2" or status == "3" or status == "4":
        assignment = 0
    # send to a hospital (if 6, more strict)
    elif status == "3" or status == "5":
        # return closest zipcodes in ascending order with matching zipcode
        # actual partial data frame
        pdf = dataframe.loc[lambda df1: df1['zip_from'] == int(zipcode)]
        # testing partial data frame
        # pdf = dataframe.loc[lambda df1: df1['zip_from'] == 40003]
        pdf = pdf.sort_values(by='distance')
        for index, row in pdf.iterrows():
            zip_to = int(row['zip_to'])
            # test print
            # print(zip_to)
            assignment = check_zip(zip_to, status)
            if assignment != -1:
                break
    elif status == "6":
        # return closest zipcodes in ascending order
        pdf = dataframe.loc[lambda df1: df1['zip_from'] == int(zipcode)]
        pdf = pdf.sort_values(by='distance')
        for index, row in pdf.iterrows():
            zip_to = int(row['zip_to'])
            # test print
            # print(zip_to)
            assignment = int(check_zip(zip_to, status))
            if assignment != -1:
                break
    return assignment


def check_zip(zipcode, status):
    # check hospitals in zip_code for open beds
    db_hospital_cursor = get_db_hospital_cursor()
    sql_query_1 = "SELECT BEDS,ï»¿ID as hospital_id FROM hospitals WHERE ZIP = " + str(zipcode)
    sql_optional = " AND trauma != \"Not Available\""

    # test print
    # if db_hospital_cursor.execute("SELECT ï»¿ID FROM hospitals WHERE ZIP = " + str(zipcode)) != 0:
    #    result = db_hospital_cursor.fetchone()
    #    print(result)
    if status == "6":
        if db_hospital_cursor.execute(sql_query_1) != 0:
            sql_response = db_hospital_cursor.fetchall()
            # print(sql_response)
            for row in sql_response:
                capacity = increment_capacity(row['hospital_id'])
                if int(capacity) < int(row['BEDS']):
                    return row['hospital_id']
        # if empty, return -1
        else:
            return -1
    else:
        if db_hospital_cursor.execute(sql_query_1) != 0:
            sql_response = db_hospital_cursor.fetchall()
            # print(sql_response)
            for row in sql_response:
                capacity = increment_capacity(row['hospital_id'])
                if int(capacity) < int(row['BEDS']):
                    return row['hospital_id']
        # if empty, return -1
        else:
            return -1
    return -1


def run_query(query):
    dbConn = get_dbConnection()
    dbCursor = get_dbCursor()
    dbCursor.execute(query)
    return dbCursor.fetchall()
