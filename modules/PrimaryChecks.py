import paramiko
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Requests import SendCommand
from modules.SSHConnection import CreateConn
from modules.Variables import deviceInfo, testResults, dataReceiver, dataSender
from classes.Utilities import Text

def CheckForMobile():    
    if (deviceInfo.sysInfo["data"]["board"]["hwinfo"]["mobile"] == False):
        raise Exception("Device does not have mobile capabilities")        
    elif (deviceInfo.sysInfo["data"]["board"]["hwinfo"]["mobile"] == True):
        print(Text.Green(
            "Device has mobile capabilities"))
        deviceInfo.mobile = True
    else:
        print(Text.Red("Could not get information about device's mobile capabilities"))
        sys.exit()


def CheckForModel(file):    
    print(
        "--Device being tested: {0}--".
        format(deviceInfo.sysInfo["data"]["mnfinfo"]["name"]))
    modelA = str(deviceInfo.sysInfo["data"]["mnfinfo"]["name"])
    try:
        modelF = file["info"]["product"]
        if(modelF == ""):
            print(Text.Red("No model was provided\nCheck JSON configuration file"))
            sys.exit()
        if modelA.startswith(modelF):
            print(Text.Green("Device model in JSON matches actual device model"))
        else:
            raise Exception("Device model in config file '{0}' and actual model '{1}' do not match\nCheck JSON configuration file".format(modelF, modelA))            
    except KeyError:
        raise Exception("Key error while reading model data\nJSON configuration file is misformed\nCheck configuration file")        


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
                print(Text.Red(
                    "Events and their messages count does not match trigger count\nCheck event type '{0}' configuration data".format(event["event-data"]["event-type"])))
                sys.exit()
        testResults.total = events
    except KeyError:
        print(Text.Red("Key error while checking events, messages and trigger count\nJSON configuration file is misformed\nCheck configuration file"))
        sys.exit()

def CheckReceiverConn():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        CreateConn(client, dataReceiver)
        time.sleep(1)
        client.close()        
    except paramiko.AuthenticationException:
        print(Text.Red("Could not reach the receiver\nCheck if device password is correct"))
        sys.exit()

def CheckSenderGsm():
    cnt = 0
    while cnt < 2:
        sim = deviceInfo.sims[cnt]
        if(sim != ""):            
            resOld = SendCommand("gsmctl -S -l all", dataSender)
            SendCommand("gsmctl -S -s \"{0} test\"".format(sim), dataSender)
            time.sleep(6)
            resNew = SendCommand("gsmctl -S -l all", dataSender)
            if (len(resNew) == len(resOld)):
                print(Text.Red("Device sent SMS to itself and did not receive the message\nCheck if phone number in configuration file is correct and if SIM card can send SMS"))
                sys.exit()
        cnt+=1    
