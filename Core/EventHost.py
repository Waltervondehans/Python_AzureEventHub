#!/user/bin/python
import sys
import azure
import socket

from azure.servicebus import (
  _service_bus_error_handler
  )

from azure.servicebus.servicebusservice import (
  ServiceBusService,
  ServiceBusSASAuthentication
  )

from azure.http import (
  HTTPRequest,
  HTTPError
  )

from azure.http.httpclient import _HTTPClient

class EventHubClient(object):

  serviceHubName=""
  eventHubName=""
  sasKeyName = ""
  sasKeyValue = ""
  def sendMessage(self,body,partition):

    eventHubHost = self.serviceHubName+".servicebus.windows.net"

    httpclient = _HTTPClient(service_instance=self)



    authentication = ServiceBusSASAuthentication(self.sasKeyName,self.sasKeyValue)

    request = HTTPRequest()
    request.method = "POST"
    request.host = eventHubHost
    request.protocol_override = "https"
    request.path = "/"+self.eventHubName+"/publishers/" + partition + "/messages?api-version=2014-05"
    request.body = body
    request.headers.append(('Content-Type', 'application/json;type=entry;charset=utf-8'))

    authentication.sign_request(request, httpclient)

    request.headers.append(('Content-Length', str(len(request.body))))

    status = 0

    try:
        resp = httpclient.perform_request(request)
        status = resp.status
    except HTTPError as ex:
        status = ex.status

    return status

class EventDataParser(object):

  def getMessage(self,payload,sensorId):
    host = socket.gethostname()
    body = "{ \"DeviceId\" : \"" + host + "\",\"SensorData\": [ "

    msgs = payload.split(",")
    first = True

    for msg in msgs:
    # print msg
      sensorType = msg.split(":")[0]
      sensorValue = msg.split(":")[1]
      if first == True:
        first = False
      else:
        body += ","

      body += "{ \"SensorId\" : \"" + sensorId + "\", \"SensorType\" : \"" + sensorType + "\", \"SensorValue\" : " + sensorValue + " }"
    body += "]}"

    return body