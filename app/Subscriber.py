#!/usr/bin/env python
import pika
import sys
import json
import DBtools


def increment_positive():
    f = open("counts.txt", "r")
    negative_count = int(f.readline())
    positive_count = int(f.readline())
    f.close()
    f = open("counts.txt", "w")
    f.write(str(negative_count + 1) + "\n" + str(positive_count))
    f.close()


def increment_negative():
    f = open("counts.txt", "r")
    negative_count = int(f.readline())
    positive_count = int(f.readline())
    f.close()
    f = open("counts.txt", "w")
    f.write(str(negative_count) + "\n" + str(positive_count + 1))
    f.close()


def get_positive_count():
    f = open("counts.txt", "r")
    negative_count = int(f.readline())
    positive_count = int(f.readline())
    f.close()
    return positive_count


def get_negative_count():
    f = open("counts.txt", "r")
    negative_count = int(f.readline())
    positive_count = int(f.readline())
    f.close()
    return negative_count


def reset_count():
    f = open("counts.txt", "w")
    f.write("0\n0")
    f.close()


DBtools.startDB()
DBtools.restartDB()
DBtools.startHospitalDB()
DBtools.reset_hospital_db()
reset_count()


def case_count(status):
    # negative test + 1
    if status == "1" or status == "4":
        increment_negative()
    # positive test + 1
    elif status == "2" or status == "5" or status == "6":
        increment_positive()
    # else not tested


# Set the connection parameters to connect to rabbit-server1 on port 5672
# on the / virtual host using the username "guest" and password "guest"

username = 'student'
password = 'student01'
hostname = '128.163.202.50'
virtualhost = '13'

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(hostname,
                                       5672,
                                       virtualhost,
                                       credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

exchange_name = 'patient_data'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = "#"

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange=exchange_name, queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    # editing to get to utf-8
    body_str = body.decode('utf-8')
    data = json.loads(body_str)

    # split payloads
    for payload in data:
        f_name = payload['first_name']
        l_name = payload['last_name']
        mrn = payload['mrn']
        zipcode = payload['zip_code']
        patient_status = payload['patient_status_code']

        # count positive and negative cases
        case_count(patient_status)
        # assign patient in mysql database
        DBtools.add_patient(f_name, l_name, mrn, zipcode, patient_status)

        # find closest open hospital, if needed. increment beds occupied
        # CODE NEEDED
        DBtools.route_patient(zipcode, patient_status)


if __name__ == '__main__':
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
