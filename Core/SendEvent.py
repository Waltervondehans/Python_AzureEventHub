import socket

import SendEvent
from Python_AzureEventHub.Core import Config


hubClient = SendEvent.EventHubClient()
#CONFIG
hubClient.serviceHubName= Config.serviceHubName
hubClient.eventHubName= Config.eventHubName
hubClient.sasKeyName= Config.sasKeyName
hubClient.sasKeyValue= Config.sasKeyValue
##CONFIG_Ende

parser = SendEvent.EventDataParser()
hostname = socket.gethostname()

i=0
while  i<100:
    sensorID="TestSensor" #beliebiger Name
    werte="z:4,l:8,x:10,y:"+str(i)#beliebig lange kommaseparierte Liste
    #Ergebnis das spaeter im EventHub liegt
    #{"DeviceId":"BINB24","SensorData":[
    #{"SensorId":"TestSensor","SensorType":"z","SensorValue":4},
    #{"SensorId":"TestSensor","SensorType":"x","SensorValue":10},
    #{"SensorId":"TestSensor","SensorType":"y","SensorValue":15}],
    # "EventProcessedUtcTime":"2015-05-06T13:42:00.3464170Z","PartitionId":5,"EventEnqueuedUtcTime":"2015-05-06T13:42:00.2470000Z"}
    body = parser.getMessage(werte,sensorID)
    hubStatus = hubClient.sendMessage(body,hostname)

    # return the HTTP status to the caller
    print hubStatus," i:",i
    i=i+1

