import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Requests import SendCommand
from variables import dataReceiver

def PurgeAllSms():
    res = SendCommand("gsmctl -S -l all", dataReceiver)
    ammount = (len(res))/15
    cnt = 0
    while cnt < ammount:
        index = res[cnt*15].split(":\t\t")[1][:-1]
        SendCommand("gsmctl -S -d {0}".format(index), dataReceiver)
        cnt += 1
