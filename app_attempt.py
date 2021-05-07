from flask import Flask
import json
import subscriber

app = Flask(__name__)


def _url(path):
    return 'http://0.0.0.0' + path


@app.route('/')
def index():
    return 'Empty Test'


@app.route('/api/reset')
def api():
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
    return jsonString


@app.route('/api/getteam')
def getteam():
    status = 1
    team_info = {
        'team_name': 'Arnoldillo',
        'Team_member_sids': str({912141777, 910823113}),
        'app_status_code': str(status)
    }
    jsonString = json.dumps(team_info)
    return jsonString


@app.route('/api/getpatient/<mrn>')
def getpatient(mrn):
    dbCursor = subscriber.DBtools.get_dbCursor()
    query = "SELECT mrn, hospital_id, " \
            " WHERE mrn is " + str(mrn)
    dbCursor.execute(query)
    return_info = dbCursor.fetchone()
    jsonString = json.dumps(return_info)
    return jsonString


@app.route('/api/gethospital/<hospital_id>')
def gethospital(hospital_id):
    dbHospitalCursor = subscriber.DBtools.get_db_hospital_cursor()
    query = "SELECT max_capacity AS total_beds," \
            " (max_capacity-current_capacity) AS available_beds," \
            " zip_code FROM hospitals" \
            " WHERE hospital_id is " + str(hospital_id)
    dbHospitalCursor.execute(query)
    return_info = dbHospitalCursor.fetchone()
    jsonString = json.dumps(return_info)
    return jsonString


@app.route('/api/testcount')
def testcount():
    return_info = {
        'positive_count': str(subscriber.get_positive_count()),
        'negative_count': str(subscriber.get_negative_count())
    }


@app.route('/api/zipalertlist')
def zipalertlist():
    # TODO
    return_info = {'Answer': 'Not implemented'}
    jsonString = json.dumps(return_info)


@app.route('/api/alertlist')
def alertlist():
    # TODO
    return_info = {'Answer': 'Not implemented'}
    jsonString = json.dumps(return_info)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int('9000'), debug=True)


def get_apis():
    return requests.get(_url('/api/'))


def describe_api(api_id):
    return requests.get(_url('/api/{:d}/'.format(api_id)))
