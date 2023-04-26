import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.Variables import eventResults, deviceInfo, fileData, testResults
from modules.FTPConnection import CreateConn
from classes.Utilities import Text

def CreateCSV(file):
    fileName = "{0}_{1}.csv".format(file["info"]["product"], testResults.startTime)
    fileInit = "echo \"Event type;Event subtype;Expected message;Received message;Sent from;Got from;Passed\" >> '{0}'".format(
        fileName)
    os.system(fileInit)
    fileData.outFileName = fileName


def UpdateCSV(index, test):        
        os.system("echo '{0};{1};{2};{3};{4};{5};{6}' >> '{7}'"
                  .format(test["event-data"]["event-type"],
                          test["event-data"]["event-subtype"][index],
                          eventResults.messageOut, eventResults.messageIn,
                          deviceInfo.sims[deviceInfo.activeSim], eventResults.received,
                          eventResults.passed, fileData.outFileName))
        


def UploadCSV():
    ftp = CreateConn()
    if(ftp != ""):
        try:
            with open(fileData.outFileName, "rb") as f:
                ftp.storbinary(f"STOR {fileData.outFileName}", f)
                ftp.quit()
            if (fileData.delete == True):
                os.system("rm '{0}'".format(fileData.outFileName))
        except FileNotFoundError:
            raise Exception("CSV result file was not found\nIt will not be uploaded to FTP server")             
