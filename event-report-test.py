import sys
from datetime import datetime
from modules.ResultFile import UploadCSV, CreateCSV
from modules.PrimaryChecks import CheckForMobile, CheckForModel, CheckTotalEvents, CheckReceiverConn, CheckSenderGsm
from modules.DataFile import ReadDataFile
from modules.APIToken import GetToken
from modules.Receiver import GetPhoneNumbers
from modules.Variables import ReadArgs, testResults, deviceInfo
from modules.TestEventsSMS import TestEvents
from modules.Requests import GetSysInfo
from classes.Utilities import Text

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
    print(Text.Underline("|   Primary checks passed   |"))
    deviceInfo.sysInfo = ""
except Exception as err:
    print(Text.Underline("|   Primary checks failed   |"))
    print(Text.Red(str(err)))
    sys.exit()
CreateCSV(data)
print("Started at: {0}".format(testResults.startTime))
print("Total tests: {0}\n".format(testResults.total))
TestEvents(data)
print("Total events tested: {0}".format(testResults.total))
print(Text.Green("Passed: {0}".format(testResults.passedCnt)), end=" ")
print(Text.Red("Failed: {0}".format(testResults.failedCnt)))
try:
    UploadCSV()
except Exception:
    print(Text.Yellow(str(err)))
print("|---------------FINISHED---------------|")