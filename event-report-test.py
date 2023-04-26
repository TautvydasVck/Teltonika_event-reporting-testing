import sys
from datetime import datetime

from classes.Utilities import Text
from modules.APIToken import GetToken
from modules.DataFile import ReadDataFile
from modules.PrimaryChecks import *
from modules.Requests import GetSysInfo
from modules.ResultFile import CreateCSV, UploadCSV
from modules.TestEventsSMS import TestEvents
from modules.Variables import ReadArgs, deviceInfo, testResults

if __name__ == "__main__":
    print(end="\n")
    testResults.startTime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    ReadArgs()
    # If one of these primary checks fails, program must be stopped
    try:
        GetToken()
        data = ReadDataFile()
        GetPhoneNumbers(data)
        GetSysInfo()
        CheckForModel(data)
        CheckForMobile()
        CheckReceiverConn()
        CheckSenderGsm()
        CheckTotalEvents(data)
        print(Text.Green("Primary checks passed"))
        deviceInfo.sysInfo = ""
    except Exception as err:
        print(Text.Red("Primary checks failed"))
        print(Text.Red(str(err)))
        sys.exit()
    CreateCSV(data)
    print("Started at: {0}".format(testResults.startTime))
    print("Total tests: {0}\n".format(testResults.total))
    TestEvents(data)
    print("Total events tested: {0}".format(testResults.total))
    print(Text.Green("Passed: {0}".format(testResults.passedCnt)), end=" ")
    print(Text.Red("Failed: {0}".format(testResults.failedCnt)))
    try
        UploadCSV()
    except Exception:
        print(Text.Yellow(str(err)))
    print("|---------------FINISHED---------------|")
