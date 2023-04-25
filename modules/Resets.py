import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Requests import SendCommand, SendEvent
from modules.Variables import dataReceiver, eventResults
from modules.Receiver import GetMessagesIndexes

def PurgeAllSms():
    res = SendCommand("gsmctl -S -l all", dataReceiver)
    indexes = GetMessagesIndexes(res)
    i = 0
    while i < len(indexes):
        SendCommand("gsmctl -S -d {0}".format(indexes[i]), dataReceiver)
        i += 1
    RecheckSms()

def RecheckSms():
    res = SendCommand("gsmctl -S -l all", dataReceiver)
    if(len(res)!=0):
        PurgeAllSms()


def PrepForNextEvent():
    SendEvent("/services/events_reporting/config/" +
                          eventResults.eventId, "", "delete")
    eventResults.passed = False
    eventResults.messageIn = ""
    eventResults.received = ""    
    PurgeAllSms()