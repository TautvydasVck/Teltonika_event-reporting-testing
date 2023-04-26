import requests
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Variables import dataSender

def GetToken():
    head = {"Content-Type": "application/json"}
    creds = {"username": dataSender.name, "password": dataSender.pswd}
    try:
        response = requests.post(
            dataSender.baseURL+"/login", json=creds,
            headers=head, timeout=20).json()
        if (response["success"] == True):
            dataSender.token = response["ubus_rpc_session"]
        else:         
            dataSender.token = ""
    except OSError:
            raise Exception(
                "Could not reach device '{dataSender.ipAddr}' to retrieve API token"
                +"\nAll following API requests will fail")
            