import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text

def GetConfigData(filePath):
    try:
        with open(filePath) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(Text.Red("JSON configuration file was not found"))
        sys.exit()
