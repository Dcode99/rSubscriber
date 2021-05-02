import json
import requests
import pymongo
import DBtools
import subscriber
import pymysql


def getAPI():
    resp = requests.get('http://deta224.cs.uky.edu:9000')
    return resp.json()


def mongo_connect():
    # Getting mongoDB setup
    # TO DO: Add database URL
    database_url = '127.0.0.1'
    client = pymongo.MongoClient(database_url)

    # Connecting to the database
    mydb = client['patients']

    # Connecting the to collection
    # TO DO: add collection name
    col = mydb[collection_name]
    d = col.delete_many()


# restart mysql database and set cursor
dbCursor = DBtools.restartDB()
# get API
path = getAPI()

# getteam API
if path is "/api/getteam":
    status = 1
    team_info = {
        'team_name': 'Arnoldillo',
        'Team_member_sids': {912141777, 910823113},
        'app_status_code': status
    }
    jsonString = json.dumps(team_info)

# reset API, needs to reset relational DB and CEP
elif path is "/api/reset":
    try:
        # Connecting the to collection
        dbCursor = DBtools.restartDB()
        return_info = {
            'reset_status_code': 1
        }
    except Exception as e:
        return_info = {
            'reset_status_code': 0
        }
    jsonString = json.dumps(return_info)

elif path is "/api/gethospital":
    query = "SELECT max_capacity AS total_beds," \
            " (max_capacity-current_capacity) AS available_beds," \
            " zip_code FROM hospitals" \
            " WHERE hospital_id is " + str(id)

    return_info = dbCursor.execute(query)
    jsonString = json.dumps(return_info)

elif path is "/api/testcount":
    return_info = {
        'positive_count': subscriber.positive_count,
        'negative_count': subscriber.negative_count
    }
    jsonString = json.dumps(return_info)
