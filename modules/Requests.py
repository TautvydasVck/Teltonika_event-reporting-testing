import paramiko
import requests
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Variables import dataSender, deviceInfo
from classes.Utilities import Text
from modules.SSHConnection import CreateConn

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
        print(Text.Red("Could not reach device '{0}' via SSH to send command".format(device.ipAddr)))
        sys.exit()


def SendTrigger(endpoint, bodyData, type):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
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
                    "To trigger event reporting rule via API use only post and put HTTP methods\nJSON file is misformed\nCheck configuration file"))
                response = {"success":False}
        return response
    except OSError:
        print(Text.Red("Could not reach device '{0}' to send trigger via API".format(dataSender.ipAddr)))
        sys.exit()    


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
                print(Text.Red(
                    "To send event report data use only post and delete HTTP methods"))
                response = {"success":False}
        return response
    except OSError:
        print(Text.Red("Could not reach device '{0}' to send event reporting data via API".format(dataSender.ipAddr)))
        sys.exit()    

def GetSysInfo():
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    try:
        response = requests.get(dataSender.baseURL +
                                "/system/device/info", headers=head, timeout=4).json()
        if (response["success"] == True):
            deviceInfo.sysInfo = response            
        else:
            print(Text.Red("Could not retrieve device system information."))
            sys.exit()
    except OSError:
        print(Text.Red("Could not reach device '{0}' to get system, hardware information via API".format(dataSender.ipAddr)))
        sys.exit()