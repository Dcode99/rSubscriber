from flask import Flask
import json
import subscriber

app = Flask(__name__)


def _url(path):
    return 'http://0.0.0.0' + path


@app.route('/')
def index():
    return 'Empty Test'


@app.route('/api/reset/')
def reset():
    try:
        # Connecting the to collection
        dbCursor = subscriber.DBtools.restartDB()
        # assign hospital capacities
        subscriber.DBtools.create_capacities()
        # reset test counts
        subscriber.reset_count()
        return_info = {
            'reset_status_code': 1
        }
    except Exception as e:
        return_info = {
            'reset_status_code': 0
        }
    jsonString = json.dumps(return_info)
    return jsonString


@app.route('/api/getteam/')
def getteam():
    status = 1
    team_info = {
        'team_name': 'Arnoldillo',
        'Team_member_sids': str({912141777, 910823113}),
        'app_status_code': str(status)
    }
    jsonString = json.dumps(team_info)
    return jsonString


@app.route('/api/getall/')
def getall():
    query = 'SELECT * from patient'
    return_info = subscriber.DBtools.run_query(query)
    print(return_info[0])
    jsonString = {
        'first_name': return_info[0]['first_name']
    }
    subscriber.DBtools.get_dbConnection().close()
    return jsonString


@app.route('/api/getpatient/<mrn>/')
def getpatient(mrn):
    subscriber.DBtools.get_dbConnection().begin()
    dbCursor = subscriber.DBtools.get_dbCursor()
    query = "SELECT mrn, hospital_id FROM patient WHERE mrn = \"" + str(mrn) + "\""
    dbCursor.execute(query)
    return_info = dbCursor.fetchall()
    subscriber.DBtools.get_dbConnection().close()
    jsonString = json.dumps(return_info)
    return jsonString


@app.route('/api/gethospital/<hospital_id>/')
def gethospital(hospital_id):
    dbHospitalCursor = subscriber.DBtools.get_db_hospital_cursor()

    query = "SELECT BEDS, ZIP FROM hospitals WHERE ï»¿ID = " + str(hospital_id)
    dbHospitalCursor.execute(query)
    return_info = dbHospitalCursor.fetchone()
    capacity = subscriber.DBtools.check_capacity(hospital_id)
    jsonString = {
        'max_capacity': str(return_info["BEDS"]),
        'available_beds': str(return_info["BEDS"] - capacity),
        'zip_code': return_info["ZIP"]
    }
    return jsonString


@app.route('/api/testcount/')
def testcount():
    jsonString = {
        'positive_count': str(subscriber.get_positive_count()),
        'negative_count': str(subscriber.get_negative_count())
    }
    return jsonString


@app.route('/api/zipalertlist/')
def zipalertlist():
    # TODO
    return_info = {'Answer': 'Not implemented'}
    jsonString = json.dumps(return_info)
    return jsonString


@app.route('/api/alertlist/')
def alertlist():
    # TODO
    return_info = {'Answer': 'Not implemented'}
    jsonString = json.dumps(return_info)
    return jsonString


# correct hostname: deta224.cs.uky.edu
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, threaded=True, debug=True)
