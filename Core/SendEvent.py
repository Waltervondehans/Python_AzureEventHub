import SendEvent
import socket
import Config

hubClient = SendEvent.EventHubClient()
#CONFIG
hubClient.serviceHubName=Config.serviceHubName
hubClient.eventHubName=Config.eventHubName
hubClient.sasKeyName=Config.sasKeyName
hubClient.sasKeyValue=Config.sasKeyValue
##CONFIG_Ende

parser = SendEvent.EventDataParser()
hostname = socket.gethostname()

i=0
while  i<100:
    sensorID="TestSensor" #beliebiger Name
    werte="z:4,l:8,x:10,y:"+str(i)#beliebig lange kommaseparierte Liste
    body = parser.getMessage(werte,sensorID)
    hubStatus = hubClient.sendMessage(body,hostname)

    # return the HTTP status to the caller
    print hubStatus," i:",i
    i=i+1