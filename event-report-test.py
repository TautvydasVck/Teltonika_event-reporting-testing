# imports
import json
import sys
import requests
from getpass import getpass
from tkinter.filedialog import askopenfilename


def Main():
    reqsData = RequestData()
    print(end="-----------\n")
    # print("Enter router's admin page credentials")
    # print("Username: ", end="")
    # name = input()
    # pswd = getpass()
    reqsData.name = "admin"
    reqsData.pswd = "Admin123"
    # print("Enter router's IP address")
    # print("IP: ", end="")
    # ipAddr = input()
    reqsData.ipAddr = "192.168.1.4"
    reqsData.baseURL = "http://"+reqsData.ipAddr+"/api/login"
    LoginToken(reqsData)
    # data = GetConfigData()
    CheckForMobile(reqsData)


def SendReq(reqsData, endpoint):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + reqsData.token}
    response = requests.post(reqsData.baseURL+endpoint, headers=head).json()
    if (response["success"] == False):
        print(Colors.Red("Request failed"))
        return -1
    else:
        print(Colors.Green("Data retrieved"))
        return response


def LoginToken(reqsData):
    head = {"Content-Type": "application/json"}
    creds = {"username": reqsData.name, "password": reqsData.pswd}
    response = requests.post(reqsData.baseURL, json=creds, headers=head).json()
    if (response["success"] == True):
        reqsData.token = response["jwtToken"]
    else:
        sys.exit("Login was unsuccessful")


def GetConfigData():
    # jsonFile = askopenfilename()
    # with open(jsonFile) as f:
    with open("/home/studentas/Documents/Python/Automated_tests/2-nd task/Teltonika_event-reporting-testing/event-config.json") as f:
        data = json.load(f)
    return data


def CheckForMobile(reqsData):
    SendReq(reqsData, "/system/device/info")
    # print(reqs["data"])
    # if (reqs["data"]["board"]["hwinfo"]["mobile"] == True):
    #    Colors.Green+"Device has mobile capabilities"
    # else:
    #    Colors.Red+"Device does not have mobile capabilities"

    # def ReadEvents(file):
    #    data = json.dumps(file)


class RequestData:
    def __init__(self):
        self.ipAddr = "",
        self.token = "",
        self.baseURL = "",
        self.name = "",
        self.pswd = ""

# Utilities


class Colors():
    def Green(text):
        return "\033[42m"+text+"\033[0m"

    def Red(text):
        return "\033[41m"+text+"\033[0m"


Main()