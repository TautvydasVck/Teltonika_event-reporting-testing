# imports
import json
import sys
import requests
import argparse
import paramiko
import time
import os
import ftplib
from datetime import datetime


def GetSysInfo():
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    response = requests.get(dataSender.baseURL +
                            "/system/device/info", headers=head).json()
    if (response["success"] == False):
        print(Text.Red("Could not retrieve device information."))
        sys.exit("Program will stop")
    else:
        return response


def GetPhoneNumbers(file):
    deviceInfo.sim1 = file["info"]["SIM1-nr"]
    deviceInfo.sim2 = file["info"]["SIM2-nr"]

def SendEvent(endpoint, bodyData, type):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    data = "{\"data\":"+bodyData+"}"
    match type:
        case "post":
            response = requests.post(dataSender.baseURL+endpoint,
                                     headers=head, data=data).json()
        case "delete":
            response = requests.delete(dataSender.baseURL+endpoint,
                                       headers=head).json()
        case _:
            print(Text.Red(
                "JSON file is misformed (missing HTTP method)\nCheck configuration file"))
            sys.exit()
    return response


def SendTrigger(endpoint, bodyData, type):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    # ATNAUJINTI TRIGERIUS (prideti  data{} api-body lauke)
    # data = "{\"data\":"+bodyData+"}"
    match type:
        case "post":
            response = requests.post(dataSender.baseURL+endpoint,
                                     headers=head, data=bodyData).json()
        case "put":
            response = requests.put(dataSender.baseURL+endpoint,
                                    headers=head, data=bodyData).json()
        case _:
            print(Text.Red(
                "JSON file is misformed (missing HTTP method)\nCheck configuration file"))
            sys.exit()
    return response


def SendCommand(data, device):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=device.ipAddr,
                   username="root", password=device.pswd, port=22)
    stdin, stdout, stderr = client.exec_command(str(data))
    client.close()
    return stdout.readlines()


def LoginToken():
    head = {"Content-Type": "application/json"}
    creds = {"username": dataSender.name, "password": dataSender.pswd}
    try:
        response = requests.post(
            dataSender.baseURL+"/login", json=creds, headers=head).json()
        if (response["success"] == True):
            dataSender.token = response["ubus_rpc_session"]
        else:
            sys.exit(Text.Red("Login was unsuccessful"))
    except OSError as err:
        print(Text.Red("Can not reach device. Program will stop"))
        print("ERROR:\n{0}".format(err))
        sys.exit()


def GetConfigData(filePath):
    with open(filePath) as f:
        data = json.load(f)
    return data


def CheckForMobile():
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
            "Device model in config file ({0}) and actual model ({1}) do not match.\nCheck JSON configuration file". format(modelF, modelA))


def CheckWhichSim():
    res = SendCommand("ubus call sim get", dataSender)
    if(res[1].__contains__('1')):
        res = deviceInfo.sim1
    elif(res[1].__contains__('2')):
        res = deviceInfo.sim2
    return res

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


def TestEvents(file):
    total = CheckTotalEvents(file)
    index = 0
    failedCnt = 0
    passedCnt = 0
    start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    CreateCSV(file, start)
    print("Started at: {0}".format(start))
    print("Total tests: {0}\n".format(total))
    for test in file["events-triggers"]:
        for subtype in test["event-data"]["event-subtype"]:
            print("Nr: {0}".format(index+1))
            print("Event type: " +
                  Text.Underline("{0}".format(test["event-data"]["event-type"])))
            print(
                "Subtype: "+Text.Underline("{0}".format(subtype)))
            eventResults.messageOut = test["event-data"]["message"][index]
            # Eventai su el. pastu yra netestuoti
            if (test["event-data"]["email-config"]["email-acc"] != ""):
                data = json.dumps({
                    ".type": "rule",
                    "enable": "1",
                    "event": test["event-data"]["event-type"],
                    "eventMark": subtype,
                    "message": test["event-data"]["message"][index],
                    "action": "sendEmail",
                    "subject": test["event-data"]["email-config"]["subject"],
                    "recipEmail": test["event-data"]["email-config"]["recievers"],
                    "emailgroup": test["event-data"]["email-config"]["email-acc"]
                })
                eventResults.sent = test["event-data"]["email-config"]["recievers"]

            elif (test["event-data"]["sms-config"]["reciever"] != "" and deviceInfo.mobile == True):
                data = json.dumps({
                    ".type": "rule",
                    "enable": "1",
                    "event": test["event-data"]["event-type"],
                    "eventMark": subtype,
                    "message": test["event-data"]["message"][index],
                    "action": "sendSMS",
                    "emailgroup": "",
                    "recipEmail": "",
                    "subject": "",
                    "recipient_format": "single",
                    "telnum": test["event-data"]["sms-config"]["reciever"]
                })
            else:
                print(Text.Red("JSON file is misformed. Check configuration file"))
                sys.exit()
            response = SendEvent(
                "/services/events_reporting/config", data, "post")
            # """
            time.sleep(2)
            if (response["success"] == True):
                eventResults.eventId = response["data"]["id"]
                TriggerEvent(test["trigger-data"][index])
                # pakeisti tikrinimo logika (durnai gauna ir tikrina gaveja)
                time.sleep(4)
                CheckReceive()
                if (eventResults.passed == True):
                    passedCnt += 1
                else:
                    failedCnt += 1
                UpdateCSV(index, test)
                time.sleep(10)
                SendEvent("/services/events_reporting/config/" +
                          eventResults.eventId, "", "delete")
            else:
                print(Text.Red("Event was not created"))
            # """
            index += 1
            print("-"*40)
        index = 0
    print("Total events tested: {0}".format(total))
    print(Text.Green("Passed: {0}".format(passedCnt)), end=" ")
    print(Text.Red("Failed: {0}".format(failedCnt)))


def TriggerEvent(trigger):
    for step in trigger["steps"]:
        match step["type"]:
            case "api":
                data = json.dumps(step["api-body"])
                time.sleep(1)
                response = SendTrigger(step["api-path"], data, step["method"])
                if (response["success"] == False):
                    print(Text.Red("Trigger using API failed"))
            case "ssh":
                data = step["command"]
                time.sleep(1)
                SendCommand(data, dataSender)
            case "cmd":
                time.sleep(1)
                os.system(step["command"])
            case "ubus":
                data = step["command"]
                data = data[:(len(data)-3)]+dataSender.token + \
                    data[(len(data)-3):]
                time.sleep(1)
                SendCommand(data, dataSender)
            case _:
                print(Text.Red("JSON file is misformed. Check configuration file"))
                sys.exit()
        pause = step["wait-time"]
        if (pause != ""):
            print(Text.Yellow(
                "Program is paused for: {0} seconds".format(pause)))
            time.sleep(int(pause))
        if (step["retrieve-token"] == "1"):
            LoginToken()


def CheckReceive():
    # pakeisti tikrinimo logika (durnai gauna ir tikrina gaveja)
    res = SendCommand("gsmctl -S -l all", dataReceiver)
    if (len(res) > 15):
        print(Text.Red("Device has old messages"))
        print("Delete all old messages and restart the test")
        sys.exit()
    elif (len(res) == 0):
        print(Text.Red("Device did not receive the message"))
    elif (len(res) == 15):
        res = SendCommand("gsmctl -S -r 0", dataReceiver)
        eventResults.received = res[2].split(":\t\t")[1][:-1]
        eventResults.messageIn = res[13].split(":\t\t")[1][:-1]        
        if (eventResults.received == CheckWhichSim()
                and eventResults.messageIn == eventResults.messageOut):
            eventResults.passed = True
            print(Text.Green("Passed"))
        else:
            print(Text.Red("Failed"))
        SendCommand("gsmctl -S -d 0", dataReceiver)
    else:
        print(Text.Red("Error reading received SMS"))


def CreateCSV(file, start):
    fileName = "\"{0}_{1}.csv\"".format(file["info"]["product"], start)
    fileInit = "echo \"Number;Event type;Event subtype;Expected message;Received message;Sent from;Got from;Passed\" >> "+fileName
    os.system(fileInit)
    eventResults.fileName = fileName


def UpdateCSV(index, test):
    os.system("echo \"{0};{1};{2};{3};{4};{5};{6};{7}\" >> {8}"
              .format(index+1, test["event-data"]["event-type"],
                      test["event-data"]["event-subtype"][index],
                      eventResults.messageOut, eventResults.messageIn,
                      eventResults.sent, eventResults.received,
                      eventResults.passed, eventResults.fileName))

"""
def UploadCSV(delete):    
    ftp.encoding = "utf-8"
    with open(eventResults.fileName) as f:
        ftp.storbinary(f"STOR {eventResults.fileName}", f)
    if (delete == True):
        os.system("rm \"{0}\"".format(eventResults.fileName))
"""
# Constructors


class DeviceData:
    def __init__(self):
        self.mobile = False
        self.smsCheck = False
        self.sim1 = ""
        self.sim2 = ""


class RequestData:
    def __init__(self):
        self.ipAddr = ""
        self.token = ""
        self.baseURL = ""
        self.name = ""
        self.pswd = ""


class ResultData:
    def __init__(self):
        self.eventId = ""
        self.passed = False
        self.messageOut = ""
        self.messageIn = ""
        self.sent = ""
        self.received = ""
        self.fileName = ""

# Utilities


class Text():
    def Green(text):
        return "\033[32m"+text+"\033[0m "

    def Red(text):
        return "\033[31m"+text+"\033[0m "

    def Yellow(text):
        return "\033[33m"+text+"\033[0m "

    def Underline(text):
        return "\033[4m"+text+"\033[0m "


# Program's main part
deviceInfo = DeviceData()
dataSender = RequestData()
dataReceiver = RequestData()
eventResults = ResultData()
# Get credentials and file path
"""
parser = argparse.ArgumentParser(
    description="Automatically test device's event reporting funcionality")
parser.add_argument(
    "-sn", "--sName", help="SMS sender device's login name", required="True")
parser.add_argument(
    "-sp", "--sPassword", help="SMS sender device's login password", required="True")
parser.add_argument(
    "-sip", "--sAddress", help="SMS sender device's IP address", required="True")
parser.add_argument(
    "-rn", "--rName", help="SMS receiver device's login name", required="True")
parser.add_argument(
    "-rp", "--rPassword", help="SMS receiver device's login password", required="True")
parser.add_argument(
    "-rip", "--rAddress", help="SMS receiver device's IP address", required="True")
parser.add_argument(
    "-file", "--configFile", help="Configuration file's path", required="True")
parser.add_argument(
    "-d", "--deleteOutput", help="Delete test results file from PC", action="store_true")
args = parser.parse_args()

dataSender.name = args.sName
dataSender.pswd = args.sPassword
dataSender.ipAddr = args.sAddress
dataSender.baseURL = "http://"+dataSender.ipAddr+"/api"

dataReceiver.name = args.rName
dataReceiver.pswd = args.rPassword
dataReceiver.ipAddr = args.rAddress
"""
dataSender.name = "admin"
dataSender.pswd = "Admin123"
dataSender.ipAddr = "192.168.1.1"
dataSender.baseURL = "http://"+dataSender.ipAddr+"/api"

dataReceiver.name = "admin"
dataReceiver.pswd = "Admin123"
dataReceiver.ipAddr = "192.168.1.1"

print(end="\n")
LoginToken()
data = GetConfigData("event-config.json")
GetPhoneNumbers(data)
#CheckWhichSim()
CheckForModel(data)
CheckForMobile()
TestEvents(data)
# UploadCSV(args.deleteOutput)
