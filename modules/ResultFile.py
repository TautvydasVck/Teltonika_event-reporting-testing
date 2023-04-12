import os
import ftplib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Variables import eventResults, deviceInfo

def CreateCSV(file, start):
    fileName = "{0}_{1}.csv".format(file["info"]["product"], start)
    fileInit = "echo \"Event type;Event subtype;Expected message;Received message;Sent from;Got from;Passed\" >> '{0}'".format(
        fileName)
    os.system(fileInit)
    eventResults.fileName = fileName


def UpdateCSV(index, test):
    os.system("echo '{0};{1};{2};{3};{4};{5};{6}' >> '{7}'"
              .format(test["event-data"]["event-type"],
                      test["event-data"]["event-subtype"][index],
                      eventResults.messageOut, eventResults.messageIn,
                      deviceInfo.sims[deviceInfo.activeSim], eventResults.received,
                      eventResults.passed, eventResults.fileName))


def UploadCSV(delete):
    ftp = ftplib.FTP(host='192.168.10.44', user='ftpuser',
                     passwd='Akademija159!')
    ftp.encoding = "utf-8"
    with open(eventResults.fileName, "rb") as f:
        ftp.storbinary(f"STOR {eventResults.fileName}", f)
    if (delete == True):
        os.system("rm '{0}'".format(eventResults.fileName))
    ftp.quit()
