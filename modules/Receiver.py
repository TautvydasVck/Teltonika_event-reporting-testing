import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Requests import SendCommand
from classes.Utilities import Text
from modules.Variables import dataReceiver, eventResults, dataSender, deviceInfo

def CheckReceive():    
    res = SendCommand("gsmctl -S -r 0", dataReceiver)    
    if (len(res) == 0):
        print(Text.Yellow("Device did not receive the message\nAfter 20 seconds program will try to read the SMS again"))
        time.sleep(20)
        res = SendCommand("gsmctl -S -r 0", dataReceiver)    
    if (len(res) >= 15):     
        CheckContent(res)    
    else:
        print(Text.Red("Device did not receive the message\nFailed"))

def CheckContent(message):    
    cnt = 14
    eventResults.received = message[2].split(":\t\t")[1][:-1]
    eventResults.messageIn+=str(message[13].split(":\t\t")[1][:-1])
    while cnt < len(message)-1:
        eventResults.messageIn+=("\n"+str(message[cnt][:-1]))
        cnt+=1    
    if (eventResults.received == deviceInfo.sims[deviceInfo.activeSim]
            and eventResults.messageIn == eventResults.messageOut):
        eventResults.passed = True
        print(Text.Green("Passed"))
    else:
        print(Text.Red("Failed"))

def GetPhoneNumbers(file):
    try:
        deviceInfo.sims[0] = file["info"]["SIM1-nr"]
        deviceInfo.sims[1] = file["info"]["SIM2-nr"]
        if(deviceInfo.sims[0] == "" and deviceInfo.sims[1] == ""):
            print(Text.Red("No SIM data was provided\nCheck configuration file"))
            sys.exit()
    except KeyError:
        print(Text.Red("Key error while reading sim data\nJSON configuration file is misformed\nCheck configuration file"))
        sys.exit()

def CheckWhichSim():
    res = SendCommand("ubus call sim get", dataSender)
    if (res[1].__contains__("1")):
        deviceInfo.activeSim = 0
    elif (res[1].__contains__("2")):
        deviceInfo.activeSim = 1    

def GetMessagesIndexes(res):
    i = 0
    indexes = []
    if(len(res)!=0):
        while i < len(res):
            if(res[i].__contains__("Index")):
                indexes.append(str(res[i]).split(":\t\t")[1][:-1])                
            i+=1
        return indexes
    else:
        return indexes