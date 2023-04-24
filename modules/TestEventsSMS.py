import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.Variables import deviceInfo, eventResults, testResults
from modules.Receiver import CheckReceive, CheckWhichSim
from modules.Triggering import TriggerEvent
from modules.Requests import SendEvent
from modules.Resets import PurgeAllSms, PrepForNextEvent
from modules.ResultFile import UpdateCSV

def TestEvents(file):
    index = 0
    try:
        for test in file["events-triggers"]:
            for subtype in test["event-data"]["event-subtype"]:
                print("Event type: " +
                      Text.Underline("{0}".format(test["event-data"]["event-type"])))
                print(
                    "Subtype: "+Text.Underline("{0}".format(subtype)))
                if (test["event-data"]["sms-config"]["reciever"] != "" and deviceInfo.mobile == True):
                    data = GetEventData(test, subtype, index)                
                    response = SendEvent(
                        "/services/events_reporting/config", data, "post")                    
                    if (response["success"] == True or response != ""):                        
                        eventResults.eventId = response["data"]["id"]
                        CheckWhichSim()
                        PurgeAllSms()
                        TriggerEvent(test["trigger-data"][index])
                        time.sleep(10)
                        CheckReceive()
                        if (eventResults.passed == True):
                            testResults.passedCnt += 1
                        UpdateCSV(index, test)
                        PrepForNextEvent()
                    else:
                        print(Text.Red("Event was not created"))
                    index += 1
                    print("-"*40)
                else:
                    print(Text.Red("JSON configuration file is misformed\nCheck configuration file"))
                    sys.exit()
            index = 0    
        testResults.failedCnt = testResults.total - testResults.passedCnt
    except KeyError:
        print(Text.Red("Key error while testing event\nJSON configuration file is misformed\nCheck configuration file"))
        sys.exit()

def GetEventData(test, subtype, index):
    try:
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
        return data
    except KeyError:
        print(Text.Red("Key error while reading event creation data\nJSON configuration file is misformed\nCheck configuration file"))
        sys.exit()