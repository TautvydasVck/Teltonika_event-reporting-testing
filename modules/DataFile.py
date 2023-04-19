import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text
from modules.Variables import fileData

def ReadDataFile():
    try:        
        return LoadFile()
    except FileNotFoundError:
        print(Text.Red("JSON configuration file was not found"))
        sys.exit()

def LoadFile():
    try:
        with open(fileData.dataFileName) as f:
                data = json.load(f)
        return data
    except json.decoder.JSONDecodeError:
         print(Text.Red("JSON file is misformed\nCheck configuration file"))
         sys.exit()
