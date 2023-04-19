import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.PrimaryChecks import CheckTotalEvents
from modules.Variables import deviceInfo, eventResults
from modules.Receiver import CheckReceive
from modules.Triggering import TriggerEvent
from modules.Requests import SendEvent
from modules.Resets import PurgeAllSms, PrepForNextEvent
from modules.ResultFile import CreateCSV, UpdateCSV

def TestEvents(file):
    total = CheckTotalEvents(file)
    index = 0
    failedCnt = 0
    passedCnt = 0
    start = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    CreateCSV(file, start)
    print("Started at: {0}".format(start))
    print("Total tests: {0}\n".format(total))
    for test in file["events-triggers"]:
        for subtype in test["event-data"]["event-subtype"]:
            print("Event type: " +
                  Text.Underline("{0}".format(test["event-data"]["event-type"])))
            print(
                "Subtype: "+Text.Underline("{0}".format(subtype)))
            if (test["event-data"]["sms-config"]["reciever"] != "" and deviceInfo.mobile == True):
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
                eventResults.messageOut = test["event-data"]["message"][index]
                response = SendEvent(
                    "/services/events_reporting/config", data, "post")
                if (response["success"] == True or response != ""):
                    eventResults.eventId = response["data"]["id"]
                    PurgeAllSms()
                    TriggerEvent(test["trigger-data"][index])
                    time.sleep(10)
                    CheckReceive()
                    if (eventResults.passed == True):
                        passedCnt += 1
                    else:
                        failedCnt += 1
                    UpdateCSV(index, test)
                    PrepForNextEvent()
                else:
                    print(Text.Red("Event was not created"))
                index += 1
                print("-"*40)
            else:
                print(Text.Red("JSON file is misformed. Check configuration file"))
                sys.exit()
        index = 0
    print("Total events tested: {0}".format(total))
    print(Text.Green("Passed: {0}".format(passedCnt)), end=" ")
    print(Text.Red("Failed: {0}".format(failedCnt)))
