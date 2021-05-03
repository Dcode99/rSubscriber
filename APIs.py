import json
import requests
from app import subscriber


def getAPI():
    resp = requests.get('http://deta224.cs.uky.edu:9000')
    return resp.json()


def run_apis(path):
    dbHospitalCursor = subscriber.DBtools.get_db_hospital_cursor()
    dbCursor = subscriber.DBtools.get_dbCursor()
    # get API
    # path = getAPI()
    jsonString = {}
    # getteam API
    if path == "/api/getteam":
        status = 1
        team_info = {
            'team_name': 'Arnoldillo',
            'Team_member_sids': str({912141777, 910823113}),
            'app_status_code': str(status)
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

        dbHospitalCursor.execute(query)
        return_info = dbHospitalCursor.fetchone()
        jsonString = json.dumps(return_info)
    elif path == "/api/testcount":
        return_info = {
            'positive_count': str(subscriber.get_positive_count()),
            'negative_count': str(subscriber.get_negative_count())
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
        mrn = path.split("/")[2]
        query = "SELECT mrn, hospital_id, " \
                " WHERE mrn is " + str(mrn)
        dbCursor.execute(query)
        return_info = dbCursor.fetchone()
        jsonString = json.dumps(return_info)
    return jsonString
