import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.Variables import dataReceiver, eventResults
from modules.Requests import SendCommand, SendEvent
from modules.Receiver import GetMessagesIndexes


def PurgeAllSms():
    try:
        res = SendCommand("gsmctl -S -l all", dataReceiver)
        indexes = GetMessagesIndexes(res)
        i = 0
        while i < len(indexes):
            SendCommand("gsmctl -S -d {0}".format(indexes[i]), dataReceiver)
            i += 1
        RecheckSms()
    except Exception as err:
        print(Text.Yellow(str(err)))


def RecheckSms():
    res = SendCommand("gsmctl -S -l all", dataReceiver)
    if (len(res) != 0):
        PurgeAllSms()


def PrepForNextEvent():
    SendEvent("/services/events_reporting/config/" +
              eventResults.eventId, "", "delete")
    eventResults.passed = False
    eventResults.messageIn = ""
    eventResults.received = ""
    eventResults.eventId = ""
    eventResults.messageOut = ""
    PurgeAllSms()
