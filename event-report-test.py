# imports
import json
import sys
import requests
from getpass import getpass
from tkinter.filedialog import askopenfilename


def Main():
    reqsData = RequestData()
    print(end="\n")
    # print("Enter router's admin page credentials")
    # print("Username: ", end="")
    # name = input()
    # pswd = getpass()
    reqsData.name = "admin"
    reqsData.pswd = "Admin123"
    # print("Enter router's IP address")
    # print("IP: ", end="")
    # ipAddr = input()
    reqsData.ipAddr = "192.168.1.1"
    reqsData.baseURL = "http://"+reqsData.ipAddr+"/api"
    LoginToken(reqsData)
    CheckForMobile(reqsData)
    data = GetConfigData()
    CreateEvents(data, reqsData)


def GetSysInfo(reqsData, endpoint):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + reqsData.token}
    response = requests.get(reqsData.baseURL+endpoint, headers=head).json()
    if (response["success"] == False):
        print(Text.Red("Request for endpoint '{0}' failed. Could not retrieve device information".format(
            endpoint)) +
            "Error: {0}. Code: {1}".format(
            response["errors"][0]["error"],
            response["errors"][0]["code"]))
        sys.exit("Program will stop")
    else:
        return response


def SendEvent(reqsData, endpoint, bodyData):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + reqsData.token}
    data = {"data": bodyData}
    response = requests.put(reqsData.baseURL+endpoint,
                            headers=head, json=data).json()
    return response


def LoginToken(reqsData):
    head = {"Content-Type": "application/json"}
    creds = {"username": reqsData.name, "password": reqsData.pswd}
    try:
        response = requests.post(
            reqsData.baseURL+"/login", json=creds, headers=head).json()
        if (response["success"] == True):
            reqsData.token = response["jwtToken"]
        else:
            sys.exit(Text.Red("Login was unsuccessful"))
    except OSError as err:
        print(Text.Red("Can not reach to device. Program will stop"))
        print("ERROR:\n{0}".format(err))
        sys.exit()


def GetConfigData():
    # jsonFile = askopenfilename()
    # with open(jsonFile) as f:
    with open("event-config.json") as f:
        data = json.load(f)
    return data


def CheckForMobile(reqsData):
    res = GetSysInfo(reqsData, "/system/device/info")
    print(
        "---Device being tested: {0}---". format(res["data"]["mnfinfo"]["name"]))
    if (res["data"]["board"]["hwinfo"]["mobile"] != True):
        print(Text.Yellow(
            "Device does not have mobile capabilities. Events can be sent only via email"))
        reqsData.mobile = False
    else:
        print(Text.Green(
            "Device has mobile capabilities. Events cant be sent via email and phone number"))
        reqsData.mobile = True


"""
--change if statement--

def CheckForModel(data, reqsData):
    res = SendGet(reqsData, "/system/device/info", "get")
    model = res["data"]["mnfinfo"]["name"]
    print(model.lower())
    print(data["info"]["product"] in model.lower())
    if data["info"]["product"] in model.lower():
        print(Colors.Green("Device model in JSON matches actual model"))
    else:
        print(Colors.Red("Device model mismatch"))
        sys.exit(
            "Device model between config file and actual model doesn not match.\nCheck JSON configuration file")
"""


def CreateEvents(json, reqsData):
    results = {}
    i = 0
    for test in json["events-triggers"]:
        print("Event: " +
              Text.Underline("{0}".format(test["event-data"]["event-type"])))
        print(
            "Subtype: "+Text.Underline("{0}".format(test["event-data"]["event-subtype"])))
        print("Current test: {0}/{1}".format(i+1, len(test)))
        data = {".type": "rule",
                "enable": "1",
                "event": test["event-data"]["event-type"],
                "eventMark": test["event-data"]["event-subtype"],
                "message": test["event-data"]["message"]}
        if (len(test["event-data"]["email-config"]["recievers"]) != 0):
            data.update({
                "action": "sendEmail",
                "subject": test["event-data"]["email-config"]["subject"],
                "recipEmail": test["event-data"]["email-config"]["recievers"],
                "eventMark": test["event-data"]["event-subtype"],
                "emailgroup": test["event-data"]["email-config"]["email-acc"]})
        elif (test["event-data"]["sms-config"]["reciever"] != ""):
            data.update({  # "action": "sendEmail",
                # "subject": test["event-data"]["email-config"]["subject"],
                # "sms-config": ""
                # "recipients": "",
                # "reciever": ""
            })        
        response = SendEvent(
            reqsData, "/services/events_reporting/config", data)
        # FillTestResults(response, results)
        if (response["success"] == True):
            print(Text.Green("Event created succesfully"))
            TriggerEvent(response, reqsData)
        else:
            print(Text.Red("Event was not created"))
        print("-"*40)
        i += 1


def TriggerEvent(json, reqsData):
    print("trigger")
# def FillTestResults(response, results):


# Constructors


class RequestData:
    def __init__(self):
        self.ipAddr = ""
        self.token = ""
        self.baseURL = ""
        self.name = ""
        self.pswd = ""
        self.mobile = False


class TestResultsData:
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


Main()
