# imports
import json
import sys
import requests
import argparse


def GetSysInfo(endpoint):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + reqsDataSender.token}
    response = requests.get(reqsDataSender.baseURL +
                            endpoint, headers=head).json()
    if (response["success"] == False):
        print(Text.Red("Could not retrieve device information."))
        sys.exit("Program will stop")
    else:
        return response


def SendEvent(endpoint, bodyData):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + reqsDataSender.token}
    data = "{\"data\":"+bodyData+"}"
    response = requests.post(reqsDataSender.baseURL+endpoint,
                             headers=head, data=data).json()
    return response


def LoginToken():
    head = {"Content-Type": "application/json"}
    creds = {"username": reqsDataSender.name, "password": reqsDataSender.pswd}
    try:
        response = requests.post(
            reqsDataSender.baseURL+"/login", json=creds, headers=head).json()
        if (response["success"] == True):
            reqsDataSender.token = response["jwtToken"]
        else:
            sys.exit(Text.Red("Login was unsuccessful"))
    except OSError as err:
        print(Text.Red("Can not reach device. Program will stop"))
        print("ERROR:\n{0}".format(err))
        sys.exit()


def GetConfigData():
    with open("event-config.json") as f:
        data = json.load(f)
    return data


def CheckForMobile():
    res = GetSysInfo("/system/device/info")
    if (res["data"]["board"]["hwinfo"]["mobile"] == False):
        print(Text.Yellow(
            "Device does not have mobile capabilities. Messages can be sent only via email"))
        reqsDataSender.mobile = False
    elif (res["data"]["board"]["hwinfo"]["mobile"] == True):
        print(Text.Green(
            "Device has mobile capabilities. Messages can be sent via email and phone number"))
        reqsDataSender.mobile = True
    else:
        print(Text.Red("Could not get information about mobile capabilities"))
        sys.exit()


def CheckForModel(data):
    res = GetSysInfo("/system/device/info")
    print(
        "--Device being tested: {0}--".
        format(res["data"]["mnfinfo"]["name"]))
    modelA = str(res["data"]["mnfinfo"]["name"])
    modelF = data["info"]["product"]
    if modelA.startswith(modelF):
        print(Text.Green("Device model in JSON matches actual device model"))
    else:
        print(Text.Red("Device model mismatch"))
        sys.exit(
            "Device model in config file ({0}) and actual model ({1}) do not match.\nCheck JSON configuration file". format(modelF, modelA))


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
    print("Total tests: {0}\n".format(events))


def CreateEvents(file):
    CheckTotalEvents(file)
    currTest = 1
    index = 0
    # results = {}
    print("Test nr: {0}".format(currTest))
    for test in file["events-triggers"]:
        for subtype in test["event-data"]["event-subtype"]:
            print("Event: " +
                  Text.Underline("{0}".format(test["event-data"]["event-type"])))
            print(
                "Subtype: "+Text.Underline("{0}".format(subtype)))
            if (test["event-data"]["email-config"] != ""):
                data = json.dumps({
                    ".type": "rule",
                    "enable": "1",
                    "event": test["event-data"]["event-type"],
                    "eventMark": test["event-data"]["event-subtype"],
                    "message": test["event-data"]["message"][index],
                    "action": "sendEmail",
                    "subject": test["event-data"]["email-config"]["subject"],
                    "recipEmail": test["event-data"]["email-config"]["recievers"],
                    "eventMark": subtype,
                    "emailgroup": test["event-data"]["email-config"]["email-acc"]
                })

            elif (test["event-data"]["sms-config"] != "" and reqsDataSender.mobile == True):
                data = json.dumps({
                    ".type": "rule",
                    "enable": "1",
                    "event": test["event-data"]["event-type"],
                    "eventMark": test["event-data"]["event-subtype"],
                    "message": test["event-data"]["message"][index],
                    "action": "sendSMS",
                    "emailgroup": "",
                    "recipEmail": "",
                    "subject": "",
                    "recipient_format": "single",
                    "telnum": test["event-data"]["sms-config"]["reciever"]
                })
            else:
                print(Text.Red("JSON file is malformed. Check configuration file"))
                sys.exit()

            response = SendEvent("/services/events_reporting/config", data)
            # print(response)
            # FillTestResults(response, results)
            if (response["success"] == False):
                print(Text.Red("Event was not created"))
            else:
                TriggerEvent(test["trigger-data"][index])
            index += 1
            currTest += 1
            print("-"*40)
        index = 0


def TriggerEvent(test):
    print(Text.Underline("Paht:{0}| JSON data: {1}".format(
        test["API-path"], test["API-body"])))
    # response = SendEvent(test["API-path"], test["API-body"])
    # if (response["success"] == False):
    #    print(Text.Red("Trigger failed"))

# def CreateCSV():
# create csv file

# def UploadCSV():
# send CSV to server via FTP

# def ClearEvents():
# delete created events from device

# Constructors


class RequestData:
    def __init__(self):
        self.ipAddr = ""
        self.token = ""
        self.baseURL = ""
        self.name = ""
        self.pswd = ""
        self.mobile = False


class TestResultData:
    def __init__(self):
        self.passed = False
        self.data = {}
        self.id = ""

# Utilities


class Text():
    def Green(text):
        return "\033[42m"+text+"\033[0m "

    def Red(text):
        return "\033[41m"+text+"\033[0m "

    def Yellow(text):
        return "\033[43m"+text+"\033[0m "

    def Underline(text):
        return "\033[4m"+text+"\033[0m "


# Program's main part
reqsDataSender = RequestData()
# reqsDataReciever = RequestData()

reqsDataSender.name = "admin"
reqsDataSender.pswd = "Admin123"
reqsDataSender.ipAddr = "192.168.1.1"
reqsDataSender.baseURL = "http://"+reqsDataSender.ipAddr+"/api"

# reqsDataReciever = reqsDataSender
# reqsDataReciever.ipAddr = "192.168.1.1"

print(end="\n")
LoginToken()
data = GetConfigData()
CheckForModel(data)
CheckForMobile()
CreateEvents(data)
