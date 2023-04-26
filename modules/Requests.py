import sys
import time
from pathlib import Path
import paramiko
import requests


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.SSHConnection import CreateConn
from modules.Variables import dataSender, deviceInfo


def SendCommand(data, device):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        CreateConn(client, device)
        stdin, stdout, stderr = client.exec_command(str(data))
        time.sleep(1)
        client.close()
        return stdout.readlines()
    except paramiko.AuthenticationException:
        raise Exception(
            "Could not connect to device '{0}' via SSH to send command"
            "\nCheck login data".format(device.ipAddr))


def SendTrigger(endpoint, bodyData, type):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    response = {"success": False}
    try:
        match type:
            case "post":
                response = requests.post(dataSender.baseURL+endpoint,
                                         headers=head, data=bodyData, timeout=10).json()
            case "put":
                response = requests.put(dataSender.baseURL+endpoint,
                                        headers=head, data=bodyData, timeout=10).json()
            case _:
                print(Text.Red(
                    "To trigger event reporting rule via API use only post and put HTTP methods"
                    "\nJSON file is misformed\nCheck configuration file"))
        if (response["success"] == False):
            print(Text.Yellow("Trigger via API failed"))
    except OSError:
        print(Text.Yellow(
            "Could not reach device '{0}'"
            " to send event reporting data via API".format(dataSender.ipAddr)))


def SendEvent(endpoint, bodyData, type):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    data = "{\"data\":"+bodyData+"}"
    try:
        match type:
            case "post":
                response = requests.post(dataSender.baseURL+endpoint,
                                         headers=head, data=data, timeout=10).json()
            case "delete":
                response = requests.delete(dataSender.baseURL+endpoint,
                                           headers=head, timeout=10).json()
            case _:
                print(Text.Yellow(
                    "To send event report data use only post and delete HTTP methods"
                    "\nCheck JSON configuration file"))
                response = {"success": False}
        return response
    except OSError:
        print(Text.Yellow(
            "Could not reach device '{0}'"
            " to send event reporting data via API".format(dataSender.ipAddr)))
        return {"success": False}


def GetSysInfo():
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    try:
        response = requests.get(dataSender.baseURL +
                                "/system/device/info", headers=head, timeout=4).json()
        if (response["success"] == True):
            deviceInfo.sysInfo = response
        else:
            raise Exception("Could not retrieve device system information")
    except OSError:
        raise Exception(
            "Could not reach device '{0}'"
            " to get system, hardware information via API".format(dataSender.ipAddr))
