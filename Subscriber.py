#!/usr/bin/env python
import pika
import sys
import DBtools
import json

positive_count = 0
negative_count = 0

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
    bodystr = body.decode('utf-8')
    data = json.loads(bodystr)
    
    # split payloads
    for payload in data:
      fname = payload['first_name']
      lname = payload['last_name']
      mrn = payload['mrn']
      zipcode = payload['zipcode']
      patient_status = payload['patient_status_code']
      
    # count positive and negative cases
    a, b = DBtools.case_count(patient_status)
    positive count += a
    negative_count += b
      
    # find closest open hospital, if needed
    # CODE NEEDED
    
    # 

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

def case_count(status):
    # negative test + 1
    if status == 1 or status == 4:
        return 0, 1
    # positive test + 1
    elif status == 2 or status == 5 or status == 6:
        return 1, 0
    # else not tested
    else:
        return 0, 0
  
 def reset_count():
    positive_count = 0
    negative_count = 0
