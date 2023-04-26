import sys
import time
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.Requests import SendCommand
from modules.Variables import (dataReceiver, dataSender, deviceInfo,
                               eventResults)


def CheckReceive():
    res = SendCommand("gsmctl -S -l all", dataReceiver)
    if (len(res) == 0):
        print(Text.Yellow(
            "Device did not receive the message"))
        print(
            "After 20 seconds program will try to read the SMS again")
        time.sleep(20)
        res = SendCommand("gsmctl -S -l all", dataReceiver)
    if (len(res) >= 15):
        LookThroughMessages(res)        
    else:
        print(Text.Yellow("Device did not receive the message"))
        print(Text.Red("Failed"))


def CheckContent(message):
    cnt = 14
    eventResults.received = message[2].split(":\t\t")[1][:-1]
    eventResults.messageIn += str(message[13].split(":\t\t")[1][:-1])
    while cnt < len(message)-1:
        eventResults.messageIn += ("\n"+str(message[cnt][:-1]))
        cnt += 1
    if (eventResults.received == deviceInfo.sims[deviceInfo.activeSim]
            and eventResults.messageIn == eventResults.messageOut):
        eventResults.passed = True    
    else:
        eventResults.received = ""
        eventResults.messageIn = ""

def LookThroughMessages(res):
    try:        
        indexes = GetMessagesIndexes(res)
        i = 0
        while i < len(indexes):
            message = SendCommand("gsmctl -S -r {0}".format(indexes[i]), dataReceiver)            
            CheckContent(message)
            if(eventResults.passed == True):
                print(Text.Green("Passed"))
                break
            i += 1        
        if(eventResults.passed == False):
            print(Text.Red("Failed"))
    except Exception as err:
        print(Text.Yellow(str(err)))

def CheckWhichSim():
    res = SendCommand("ubus call sim get", dataSender)
    if (res[1].__contains__("1")):
        deviceInfo.activeSim = 0
    elif (res[1].__contains__("2")):
        deviceInfo.activeSim = 1


def GetMessagesIndexes(res):
    i = 0
    indexes = []
    while i < len(res):
        if (res[i].__contains__("Index")):
            indexes.append(str(res[i]).split(":\t\t")[1][:-1])
        i += 1
    return indexes
