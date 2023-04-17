import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.DeviceData import DeviceData
from classes.RequestData import RequestData
from classes.ResultData import ResultData
from classes.Files import Files

deviceInfo = DeviceData()
dataSender = RequestData()
dataReceiver = RequestData()
eventResults = ResultData()
fileData = Files()

def ReadArgs():
    parser = argparse.ArgumentParser(
    description="Automatically test device's event reporting funcionality")
    parser.add_argument(
        "-sn", "--sName", help="SMS sender device's login name. Default: admin", action="store", default="admin")
    parser.add_argument(
        "-sp", "--sPassword", help="SMS sender device's login password. Default: Admin123", action="store", default="Admin123")
    parser.add_argument(
        "-sip", "--sAddress", help="SMS sender device's IP address. Default: 192.168.1.1", action="store", default="192.168.1.1")    
    parser.add_argument(
        "-rp", "--rPassword", help="SMS receiver device's login password. Default: Admin123", action="store", default="Admin123")
    parser.add_argument(
        "-rip", "--rAddress", help="SMS receiver device's IP address. Default: 192.168.1.1", action="store", default="192.168.1.8")
    parser.add_argument(
        "-file", "--configFile", help="Configuration file's path. Default: ./event-config.json", action="store", default="event-config.json")
    parser.add_argument(
        "-d", "--deleteFile", help="Delete test results file from PC. Default: false", action="store_true", default=False)
    args = parser.parse_args()

    dataSender.name = args.sName
    dataSender.pswd = args.sPassword
    dataSender.ipAddr = args.sAddress
    dataSender.baseURL = "http://"+dataSender.ipAddr+"/api"

    dataReceiver.pswd = args.rPassword
    dataReceiver.ipAddr = args.rAddress

    fileData.dataFileName =args.configFile
    fileData.delete = args.deleteFile