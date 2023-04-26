import sys
import time
from pathlib import Path
import paramiko

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.Requests import SendCommand
from modules.SSHConnection import CreateConn
from modules.Resets import PurgeAllSms
from modules.Variables import dataReceiver, dataSender, deviceInfo, testResults


def CheckForMobile():
    if (deviceInfo.sysInfo["data"]["board"]["hwinfo"]["mobile"] == False):
        raise Exception("Device does not have mobile capabilities")
    elif (deviceInfo.sysInfo["data"]["board"]["hwinfo"]["mobile"] == True):
        print(Text.Green(
            "Device has mobile capabilities"))
        deviceInfo.mobile = True
    else:
        raise Exception(
            "Could not get information about device's mobile capabilities")


def GetPhoneNumbers(file):
    try:
        deviceInfo.sims[0] = file["info"]["SIM1-nr"]
        deviceInfo.sims[1] = file["info"]["SIM2-nr"]
        if (deviceInfo.sims[0] == "" and deviceInfo.sims[1] == ""):
            raise Exception(
                "No SIM data was provided\nCheck configuration file")
    except KeyError:
        raise Exception(
            "Key error while reading sim data\nJSON configuration file is misformed"
            "\nCheck configuration file")


def CheckForModel(file):
    print(
        "--Device being tested: {0}--".
        format(deviceInfo.sysInfo["data"]["mnfinfo"]["name"]))
    modelA = str(deviceInfo.sysInfo["data"]["mnfinfo"]["name"])
    try:
        modelF = file["info"]["product"]
        if (modelF == ""):
            raise Exception(
                "No model was provided\nCheck JSON configuration file")
        if modelA.startswith(modelF):
            print(Text.Green("Device model in JSON matches actual device model"))
        else:
            raise Exception(
                "Device model in config file '{0}' and actual model '{1}' do not match"
                "\nCheck JSON configuration file".format(modelF, modelA))
    except KeyError:
        raise Exception(
            "Key error while reading model data\nJSON configuration file is misformed"
            "\nCheck configuration file")


def CheckTotalEvents(file):
    events = 0
    triggers = 0
    messages = 0
    try:
        for event in file["events-triggers"]:
            events += len(event["event-data"]["event-subtype"])
            triggers += len(event["trigger-data"])
            messages += len(event["event-data"]["message"])
            if (events != triggers or events != messages):
                raise Exception(
                    "Events and their messages count does not match trigger count"
                    "\nCheck event type '{0}' configuration data"
                    .format(event["event-data"]["event-type"]))
        testResults.total = events
    except KeyError:
        raise Exception(
            "Key error while checking events, messages and trigger count"
            "\nJSON configuration file is misformed\nCheck configuration file")


def CheckReceiverConn():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        CreateConn(client, dataReceiver)
        time.sleep(1)
        client.close()
    except paramiko.AuthenticationException:
        raise Exception(
            "Could not reach the receiver\nCheck if device password is correct")


def CheckSenderGsm():    
    cnt = 0
    gotMessage = False
    while cnt < 2:
        sim = deviceInfo.sims[cnt]
        if (sim != ""):
            resOld = SendCommand("gsmctl -S -l all", dataSender)
            SendCommand("gsmctl -S -s \"{0} test\"".format(sim), dataSender)
            time.sleep(6)
            resNew = SendCommand("gsmctl -S -l all", dataSender)
            if (len(resNew) > len(resOld)):
                gotMessage = True                
        cnt += 1
    PurgeAllSms(dataSender)
    if(gotMessage == False):
        raise Exception(
                "Device sent SMS to itself and did not receive the message"
                "\nCheck if phone number in configuration file is correct"
                " and if SIM card can send SMS")
