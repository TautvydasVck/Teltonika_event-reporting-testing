# imports
import json
import requests
from getpass import getpass
from tkinter.filedialog import askopenfilename

# main function with user login


def Main():
    print(end="-----------\n")
    token = LoginToDevice()
    data = GetConfigData()
    # print("value: {}".format(jsonFile))


def GetConfigData():
    # jsonFile = askopenfilename()
    # with open(jsonFile) as f:
    with open("/home/studentas/Documents/Python/Automated_tests/2-nd task/Teltonika_event-reporting-testing/event-config.json") as f:
        data = json.load(f)
    return data


def LoginToDevice():
    # print("Enter router's admin page credentials")
    # print("Username: ", end="")
    # name = input()
    # pswd = getpass()
    name = "admin"
    pswd = "Admin123"
    # print("Enter router's IP address")
    # print("IP: ", end="")
    # ipAddr = input()
    ipAddr = "192.168.1.1"

    url = "http://"+ipAddr+"/api/login"
    creds = {"username": name, "password": pswd}
    response = requests.post(url, json=creds).json()
    return response["jwtToken"]


def CheckForMobile(ip, data):
    # device's info
    model = data["info"]["product"]

# def ReadEvents(file):
#    data = json.dumps(file)


Main()
