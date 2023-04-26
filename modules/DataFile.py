import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Variables import fileData

def ReadDataFile():
    try:        
        return LoadFile()
    except FileNotFoundError:
        raise Exception("Error while loading configuration file\nProvided JSON configuration file was not found\nProgram stopped")        

def LoadFile():
    try:
        with open(fileData.dataFileName) as f:
                data = json.load(f)
        return data
    except json.decoder.JSONDecodeError:
        raise Exception("Error while loading configuration file\nJSON configuration file is misformed\nProgram stopped")        
