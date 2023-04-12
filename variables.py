from classes.DeviceData import DeviceData
from classes.RequestData import RequestData
from classes.ResultData import ResultData

deviceInfo = DeviceData()
dataSender = RequestData()
dataReceiver = RequestData()
eventResults = ResultData()

dataSender.name = "admin"
dataSender.pswd = "Admin123"
dataSender.ipAddr = "192.168.1.1"
dataSender.baseURL = "http://"+dataSender.ipAddr+"/api"

dataReceiver.name = "admin"
dataReceiver.pswd = "Admin123"
dataReceiver.ipAddr = "192.168.1.1"