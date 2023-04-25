import paramiko
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text

def CreateConn(client, device):
    try:
        client.connect(hostname=device.ipAddr,
                           username="root", password=device.pswd, port=22, timeout=4)
    except OSError:
        print(Text.Red("Unable to connect to device '{0}' via SSH".format(device.ipAddr)))
        sys.exit()
    