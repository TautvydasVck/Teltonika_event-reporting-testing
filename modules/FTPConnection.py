import ftplib
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from classes.Utilities import Text


def CreateConn():
    try:
        ftp = ftplib.FTP(host="", user="",
                         passwd="", timeout=20)
        ftp.encoding = "utf-8"
        return ftp
    except ftplib.all_errors:
        ftp.close()
        print(Text.Red("Could not connect to FTP server"
                       "\nResult file will not be uploaded"))
        return ""
