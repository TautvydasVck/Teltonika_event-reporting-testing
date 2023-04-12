import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.Variables import dataSender
from classes.Utilities import Text

def GetToken():
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