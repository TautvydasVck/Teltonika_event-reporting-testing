import json
import sys
import time
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.MessageDecode import Decode
from modules.Receiver import CheckReceive, CheckWhichSim
from modules.Requests import SendEvent
from modules.Resets import PrepForNextEvent, PurgeAllSms
from modules.ResultFile import UpdateCSV
from modules.Triggering import TriggerEvent
from modules.Variables import deviceInfo, eventResults, testResults, dataReceiver


def TestEvents(file):
    index = 0
    for test in file["events-triggers"]:
        for subtype in test["event-data"]["event-subtype"]:
            print("Event type: " +
                  Text.Underline("{0}".format(test["event-data"]["event-type"])))
            print(
                "Subtype: "+Text.Underline("{0}".format(subtype)))
            if (test["event-data"]["sms-config"]["reciever"] != ""
                    and deviceInfo.mobile == True):
                data = GetEventData(test, subtype, index)
                response = SendEvent(
                    "/services/events_reporting/config", data, "post")
                if (response["success"] == True):
                    eventResults.eventId = response["data"]["id"]
                    try:                        
                        CheckWhichSim()
                        PurgeAllSms(dataReceiver)
                        TriggerEvent(test["trigger-data"][index])
                        time.sleep(10)
                        CheckReceive()
                        if (eventResults.passed == True):
                            testResults.passedCnt += 1                                                
                    except Exception as err:
                        eventResults.passed = False
                        print(Text.Yellow(str(err)))
                        print(Text.Red("Failed"))                        
                    finally:                        
                        UpdateCSV(index, test)
                        PrepForNextEvent()
                else:
                    eventResults.passed = False
                    print(Text.Yellow("Event was not created"))
                    print(Text.Red("Failed"))
                    UpdateCSV(index, test)
                    PrepForNextEvent()
                index += 1
                print("-"*40)
            else:
                print(Text.Red("JSON configuration file is misformed"
                               "\nCheck configuration file"))
                sys.exit()
        index = 0
    testResults.failedCnt = testResults.total - testResults.passedCnt


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
        Decode()
        return data
    except KeyError:
        print(Text.Yellow("Key error in event report configuration"
                          "\nEvent with this data might not be created"))
