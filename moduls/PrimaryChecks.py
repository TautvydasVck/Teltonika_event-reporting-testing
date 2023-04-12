import sys
import requests

from classes.Utilities import Text


def GetSysInfo(dataSender):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    response = requests.get(dataSender.baseURL +
                            "/system/device/info", headers=head).json()
    if (response["success"] == False):
        print(Text.Red("Could not retrieve device information."))
        sys.exit("Program will stop")
    else:
        return response


def CheckForMobile(deviceInfo):
    res = GetSysInfo()
    if (res["data"]["board"]["hwinfo"]["mobile"] == False):
        print(Text.Yellow(
            "Device does not have mobile capabilities. Messages can be sent only via email"))
        deviceInfo.mobile = False
    elif (res["data"]["board"]["hwinfo"]["mobile"] == True):
        print(Text.Green(
            "Device has mobile capabilities. Messages can be sent via email and phone number"))
        deviceInfo.mobile = True
    else:
        print(Text.Red("Could not get information about mobile capabilities"))
        sys.exit()


def CheckForModel(file):
    res = GetSysInfo()
    print(
        "--Device being tested: {0}--".
        format(res["data"]["mnfinfo"]["name"]))
    modelA = str(res["data"]["mnfinfo"]["name"])
    modelF = file["info"]["product"]
    if modelA.startswith(modelF):
        print(Text.Green("Device model in JSON matches actual device model"))
    else:
        print(Text.Red("Device model mismatch"))
        sys.exit(
            "Device model in config file ({0}) and actual model ({1}) do not match.\n" +
            "Check JSON configuration file". format(modelF, modelA))

def CheckTotalEvents(file):
    events = 0
    triggers = 0
    messages = 0
    for event in file["events-triggers"]:
        events += len(event["event-data"]["event-subtype"])
        triggers += len(event["trigger-data"])
        messages += len(event["event-data"]["message"])
        if (events != triggers or events != messages):
            print(Text.Red(
                "Events and their messages count does not match trigger count. Check JSON configuration file"))
            sys.exit()
    return events