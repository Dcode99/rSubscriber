from PySiddhi.core.SiddhiManager import SiddhiManager
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent


siddhiManager = SiddhiManager()

#Define Siddhi query
patientStream = "define stream PatientStream (first_name string, last_name string, mrn int, zip_code int, patient_status_code int); " + \
		"@info(name = 'mid') from PatientStream#window.time(15 sec) as f join PatientStream#window.time(30 sec) as t on f.zip_code == t.zip_code select f.zip_code as zip, f.count() as fCount, t.count() as tCount insert into MidStream; " + \
		"@info(name = 'zipalert') from MidStream[3*fCount > 2*tCount] select zip insert into OutputStream; " + \
		"@info(name = 'statealert') from OutputStream#window.time(15 sec) select count() as EmergencyZipCount having EmergencyZipCount > 4 insert into StateStream; "

#Generate runtime
patientRuntime = siddhiManager.createSiddhiAppRuntime(patientStream)


#Listener
class QueryCallbackImpl(QueryCallback):
	def receive(self, timestamp, inEvents, outEvents):
		PrintEvent(timestamp, inEvents, outEvents)

#Add listener for stream that alerts when a zip code experiences growth
patientRuntime.addCallback("zipalert", QueryCallbackImpl())

#Add listener for stream that alerts when five or more zip codes are in alert state
patientRuntime.addCallback("statealert", QueryCallbackImpl())

#input handler that processes events to siddhi
inputHandler = patientRuntime.getInputHandler("PatientStream")

#Start event processing
patientRuntime.start()

inputHandler.send("Nathan", "Arnold", 1, 40508, 6)

#shut down when all event processing is finished
siddhiManager.shutdown()
