import ftplib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text

def CreateConn():
    try:
        ftp = ftplib.FTP(host="192.168.10.44", user="ftpuser", passwd="Akademija159!")
        ftp.encoding = "utf-8"
        return ftp
    except OSError:
        print(Text.Red("Error while establishing connection to server\nCould not connect to FTP server\nResult file will not be uploaded"))
        return ""