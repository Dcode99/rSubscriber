from PySiddhi.core.SiddhiManager import SiddhiManager
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.uttil.EventPrinter import PrintEvent


siddhiManager = SiddhiManager()

#Define Siddhi query
patientStream = "define stream PatientStream (first_name string, last_name string, mrn int, zip_code int, patient_status_code int); " + \
		"@info(name = 'status') from PatientStream#window.time(15 sec) as f join PatientStream#window.time(30 sec) as t on f.zip_code == t.zip_code select f.count() as fCount, t.count() as tCount insert into OutputStream;"

#Generate runtime
patientRuntime = siddhiManager.createSiddhiAppRuntime(patientStream)


#Listener
class QueryCallbackImpl(QueryCallback):
	def receive(self, timestamp, inEvents, outEvents):
		PrintEvent(timestamp, inEvents, outEvents)
patientRuntime.addCallback("status", QueryCallbackImpl())


#input handler that processes events to siddhi
inputHandler = patientRuntime.getInputHandler("PatientStream")

#Start event processing
patientRuntime.start()

inputHandler.send("Nathan", "Arnold", 1, 40508, 6)

#shut down when all event processing is finished
siddhiManager.shutdown()
