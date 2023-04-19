import time
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.Requests import SendCommand, SendTrigger
from modules.APIToken import GetToken
from modules.Variables import dataSender

def TriggerEvent(trigger):    
    for step in trigger["steps"]:
        match step["type"]:
            case "api":
                time.sleep(1)
                response = SendTrigger(
                    step["api-path"], json.dumps(step["api-body"]), step["method"])
                if (response["success"] == False or response == ""):
                    print(Text.Yellow("Trigger using API failed"))
            case "ssh":
                SendCommand(step["command"], dataSender)
            case "cmd":
                time.sleep(1)
                os.system(step["command"])
            case "ubus":
                data = step["command"]
                data = data[:(len(data)-3)]+dataSender.token + \
                    data[(len(data)-3):]
                SendCommand(data, dataSender)
            case _:
                print(Text.Red("JSON configuration file is misformed\nCheck configuration file"))
                sys.exit()
        pause = step["wait-time"]
        if (pause != ""):
            print(Text.Yellow(
                "Paused for additional: {0} sec.".format(pause)))
            time.sleep(int(pause))
        if (step["retrieve-token"] == "1"):
            GetToken()
