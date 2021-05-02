import json
import requests
import pymysql
import subscriber


def getAPI():
    resp = requests.get('http://deta224.cs.uky.edu:9000')
    return resp.json()


def run_apis():
    # restart mysql database and set cursor
    dbCursor = subscriber.DBtools.restartDB()
    # get API
    path = getAPI()
    jsonString = {}
    # getteam API
    if path == "/api/getteam":
        status = 1
        team_info = {
            'team_name': 'Arnoldillo',
            'Team_member_sids': {912141777, 910823113},
            'app_status_code': status
        }
        jsonString = json.dumps(team_info)

    # reset API, needs to reset relational DB and CEP
    elif path == "/api/reset":
        try:
            # Connecting the to collection
            dbCursor = subscriber.DBtools.restartDB()
            return_info = {
                'reset_status_code': 1
            }
        except Exception as e:
            return_info = {
                'reset_status_code': 0
            }
        jsonString = json.dumps(return_info)
    elif path.split("/")[1] == "/api/gethospital":
        hospital_id = path.split("/")[2]
        query = "SELECT max_capacity AS total_beds," \
                " (max_capacity-current_capacity) AS available_beds," \
                " zip_code FROM hospitals" \
                " WHERE hospital_id is " + str(hospital_id)

        return_info = dbCursor.execute(query)
        jsonString = json.dumps(return_info)

    elif path == "/api/testcount":
        return_info = {
            'positive_count': subscriber.positive_count,
            'negative_count': subscriber.negative_count
        }
        jsonString = json.dumps(return_info)
    elif path == "/api/zipalertlist":
        # TODO
        return_info = {}
        jsonString = json.dumps(return_info)
    elif path == "/api/alertlist":
        # TODO
        return_info = {}
        jsonString = json.dumps(return_info)
    elif path.split("/")[1] == "getpatient":
        # TODO
        return_info = {}
        jsonString = json.dumps(return_info)
    return jsonString


print("Bottom of APIs.py")
