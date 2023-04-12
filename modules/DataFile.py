import json


def GetConfigData(filePath):
    with open(filePath) as f:
        data = json.load(f)
    return data
