# systemic imports
import json
import sys
import time
from datetime import datetime

# created modules
from modules.ResultFile import CreateCSV, UpdateCSV, UploadCSV
from modules.PrimaryChecks import CheckForMobile, CheckForModel, CheckTotalEvents
from modules.DataFile import GetConfigData
from modules.Resets import PurgeAllSms
from modules.Requests import SendEvent
from modules.APIToken import GetToken
from modules.Triggering import TriggerEvent
from modules.Receiver import CheckReceive, GetPhoneNumbers
# created classes
from classes.Utilities import Text
from variables import deviceInfo, eventResults


def TestEvents(file):
    total = CheckTotalEvents(file)
    index = 0
    failedCnt = 0
    passedCnt = 0
    start = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    CreateCSV(file, start)
    print("Started at: {0}".format(start))
    print("Total tests: {0}\n".format(total))
    PurgeAllSms()
    for test in file["events-triggers"]:
        for subtype in test["event-data"]["event-subtype"]:
            print("Event type: " +
                  Text.Underline("{0}".format(test["event-data"]["event-type"])))
            print(
                "Subtype: "+Text.Underline("{0}".format(subtype)))
            eventResults.messageOut = test["event-data"]["message"][index]
            # Eventai su el. pastu yra netestuoti
            if (test["event-data"]["email-config"]["email-acc"] != ""):
                data = json.dumps({
                    ".type": "rule",
                    "enable": "1",
                    "event": test["event-data"]["event-type"],
                    "eventMark": subtype,
                    "message": test["event-data"]["message"][index],
                    "action": "sendEmail",
                    "subject": test["event-data"]["email-config"]["subject"],
                    "recipEmail": test["event-data"]["email-config"]["recievers"],
                    "emailgroup": test["event-data"]["email-config"]["email-acc"]
                })
                eventResults.sent = test["event-data"]["email-config"]["recievers"]

            elif (test["event-data"]["sms-config"]["reciever"] != "" and deviceInfo.mobile == True):
                data = json.dumps({
                    ".type": "rule",
                    "enable": "1",
                    "event": test["event-data"]["event-type"],
                    "eventMark": subtype,
                    "message": test["event-data"]["message"][index],
                    "action": "sendSMS",
                    "emailgroup": "",
                    "recipEmail": "",
                    "subject": "",
                    "recipient_format": "single",
                    "telnum": test["event-data"]["sms-config"]["reciever"]
                })
            else:
                print(Text.Red("JSON file is misformed. Check configuration file"))
                sys.exit()
            response = SendEvent(
                "/services/events_reporting/config", data, "post")
            time.sleep(2)
            # """
            if (response["success"] == True):
                eventResults.eventId = response["data"]["id"]
                TriggerEvent(test["trigger-data"][index])
                time.sleep(10)
                CheckReceive()
                if (eventResults.passed == True):
                    passedCnt += 1
                else:
                    failedCnt += 1
                UpdateCSV(index, test)
                # nuresetinimas, evento istrynimas
                SendEvent("/services/events_reporting/config/" +
                          eventResults.eventId, "", "delete")
                eventResults.passed = False
                PurgeAllSms()
            else:
                print(Text.Red("Event was not created"))
            # """
            index += 1
            print("-"*40)
        index = 0
    print("Total events tested: {0}".format(total))
    print(Text.Green("Passed: {0}".format(passedCnt)), end=" ")
    print(Text.Red("Failed: {0}".format(failedCnt)))

# Program's main part
# Get credentials and file path
"""
parser = argparse.ArgumentParser(
    description="Automatically test device's event reporting funcionality")
parser.add_argument(
    "-sn", "--sName", help="SMS sender device's login name", required="True")
parser.add_argument(
    "-sp", "--sPassword", help="SMS sender device's login password", required="True")
parser.add_argument(
    "-sip", "--sAddress", help="SMS sender device's IP address", required="True")
parser.add_argument(
    "-rn", "--rName", help="SMS receiver device's login name", required="True")
parser.add_argument(
    "-rp", "--rPassword", help="SMS receiver device's login password", required="True")
parser.add_argument(
    "-rip", "--rAddress", help="SMS receiver device's IP address", required="True")
parser.add_argument(
    "-file", "--configFile", help="Configuration file's path", required="True")
parser.add_argument(
    "-d", "--deleteOutput", help="Delete test results file from PC", action="store_true")
args = parser.parse_args()

dataSender.name = args.sName
dataSender.pswd = args.sPassword
dataSender.ipAddr = args.sAddress
dataSender.baseURL = "http://"+dataSender.ipAddr+"/api"

dataReceiver.name = args.rName
dataReceiver.pswd = args.rPassword
dataReceiver.ipAddr = args.rAddress
"""
print(end="\n")
GetToken()
data = GetConfigData("event-config.json")
GetPhoneNumbers(data)
CheckForModel(data)
CheckForMobile()
TestEvents(data)
UploadCSV(False)
