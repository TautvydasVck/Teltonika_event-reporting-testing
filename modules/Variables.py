from classes.TestResultData import TestResultData
from classes.Files import Files
from classes.EventResultData import EventResultData
from classes.RequestData import RequestData
from classes.DeviceData import DeviceData
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

deviceInfo = DeviceData()
dataSender = RequestData()
dataReceiver = RequestData()
eventResults = EventResultData()
testResults = TestResultData()
fileData = Files()


def ReadArgs():
    parser = argparse.ArgumentParser(
        description="Automatically test device's event reporting funcionality")
    parser.add_argument(
        "-sn", "--sName", help="SMS sender device login name. Default: admin", action="store", default="admin")
    parser.add_argument(
        "-sp", "--sPassword", help="SMS sender device login password. Default: Admin123", action="store", default="Admin123")
    parser.add_argument(
        "-sip", "--sAddress", help="SMS sender device IP address. Default: 192.168.1.1", action="store", default="192.168.1.1")
    parser.add_argument(
        "-rp", "--rPassword", help="SMS receiver device login password. Default: Admin123", action="store", default="Admin123")
    parser.add_argument(
        "-rip", "--rAddress", help="SMS receiver device IP address. Default: 192.168.1.2", action="store", default="192.168.1.2")
    parser.add_argument(
        "-f", "--configFile", help="Configuration file path. Default: ./event-config.json", action="store", default="event-config.json")
    parser.add_argument(
        "-d", "--deleteFile", help="Delete test result file from PC. Default: false", action="store_true", default=False)
    args = parser.parse_args()

    dataSender.name = args.sName
    dataSender.pswd = args.sPassword
    dataSender.ipAddr = args.sAddress
    dataSender.baseURL = "http://"+dataSender.ipAddr+"/api"

    dataReceiver.pswd = args.rPassword
    dataReceiver.ipAddr = args.rAddress

    fileData.dataFileName = args.configFile
    fileData.delete = args.deleteFile
