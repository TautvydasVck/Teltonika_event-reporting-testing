import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Requests import SendCommand
from classes.Utilities import Text
from variables import dataReceiver, eventResults, dataSender, deviceInfo

def CheckReceive():
    CheckWhichSim()
    res = SendCommand("gsmctl -S -l all", dataReceiver)
    if (len(res) == 0):
        print(Text.Red("Device did not receive the message"))
    elif (len(res) >= 15):
        eventResults.received = res[2].split(":\t\t")[1][:-1]
        eventResults.messageIn = res[13].split(":\t\t")[1][:-1]
        if (eventResults.received == deviceInfo.sims[deviceInfo.activeSim]
                and eventResults.messageIn == eventResults.messageOut):
            eventResults.passed = True
            print(Text.Green("Passed"))
        else:
            print(Text.Red("Failed"))

    else:
        print(Text.Red("Error reading received SMS"))

def CheckWhichSim():
    res = SendCommand("ubus call sim get", dataSender)
    if (res[1].__contains__('1')):
        deviceInfo.activeSim = 0
    elif (res[1].__contains__('2')):
        deviceInfo.activeSim = 1

def GetPhoneNumbers(file):
    deviceInfo.sims[0] = file["info"]["SIM1-nr"]
    deviceInfo.sims[1] = file["info"]["SIM2-nr"]