import paramiko
import requests
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Variables import dataSender
from classes.Utilities import Text

def SendCommand(data, device):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=device.ipAddr,
                       username="root", password=device.pswd, port=22)
        stdin, stdout, stderr = client.exec_command(str(data))
        time.sleep(1)
        client.close()
        return stdout.readlines()
    except paramiko.AuthenticationException:
        print(Text.Red("Could not reach device"))
        sys.exit()


def SendTrigger(endpoint, bodyData, type):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    match type:
        case "post":
            response = requests.post(dataSender.baseURL+endpoint,
                                     headers=head, data=bodyData, timeout=10).json()
        case "put":
            response = requests.put(dataSender.baseURL+endpoint,
                                    headers=head, data=bodyData, timeout=10).json()
        case _:
            print(Text.Red(
                "JSON file is misformed (Trigger is missing HTTP method)\nCheck configuration file"))
            response = ""
    return response


def SendEvent(endpoint, bodyData, type):
    head = {"Content-Type": "application/json",
            "Authorization": "Bearer " + dataSender.token}
    data = "{\"data\":"+bodyData+"}"
    match type:
        case "post":
            response = requests.post(dataSender.baseURL+endpoint,
                                     headers=head, data=data, timeout=10).json()
        case "delete":
            response = requests.delete(dataSender.baseURL+endpoint,
                                       headers=head, timeout=10).json()
        case _:
            print(Text.Red(
                "JSON file is misformed (Event is missing HTTP method)\nCheck configuration file"))
            sys.exit()
    return response
