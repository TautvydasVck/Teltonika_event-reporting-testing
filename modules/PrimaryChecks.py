import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Variables import deviceInfo, testResults
from classes.Utilities import Text

def CheckForMobile():    
    if (deviceInfo.sysInfo["data"]["board"]["hwinfo"]["mobile"] == False):
        print(Text.Red(
            "Device does not have mobile capabilities"))
        # deviceInfo.mobile = False
        sys.exit()
    elif (deviceInfo.sysInfo["data"]["board"]["hwinfo"]["mobile"] == True):
        print(Text.Green(
            "Device has mobile capabilities"))
        deviceInfo.mobile = True
    else:
        print(Text.Red("Could not get information about mobile capabilities"))
        sys.exit()


def CheckForModel(file):    
    print(
        "--Device being tested: {0}--".
        format(deviceInfo.sysInfo["data"]["mnfinfo"]["name"]))
    modelA = str(deviceInfo.sysInfo["data"]["mnfinfo"]["name"])
    try:
        modelF = file["info"]["product"]
        if modelA.startswith(modelF):
            print(Text.Green("Device model in JSON matches actual device model"))
        else:
            print(Text.Red("Device model mismatch"))
            sys.exit(
                "Device model in config file ({0}) and actual model ({1}) do not match.\n" +
                "Check JSON configuration file". format(modelF, modelA))
    except KeyError:
        print(Text.Red("JSON configuration file is misformed\nCheck configuration file"))
        sys.exit()


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
                    "Events and their messages count does not match trigger count\nCheck JSON configuration file"))
                sys.exit()
        testResults.total = events
    except KeyError:
        print(Text.Red("JSON configuration file is misformed\nCheck configuration file"))
        sys.exit()
