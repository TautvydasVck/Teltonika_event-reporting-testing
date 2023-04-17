import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Variables import dataSender, eventResults
from modules.Requests import SendCommand

def Decode():
    if(eventResults.messageOut.__contains__("%ie")):
        res = SendCommand("gsmctl -i", dataSender)
        eventResults.messageOut.replace("%ie", res[0][:-1])
               