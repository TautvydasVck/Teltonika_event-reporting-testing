import paramiko
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text

def CreateConn(client, device):
    try:
        client.connect(hostname=device.ipAddr, username="root",
                    password=device.pswd, port=22, timeout=20)
    except OSError:
        client.close()
        raise Exception("Unable to reach device '{0}' via SSH".format(device.ipAddr))        
    