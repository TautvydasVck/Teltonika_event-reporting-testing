from modules.ResultFile import UploadCSV
from modules.PrimaryChecks import CheckForMobile, CheckForModel
from modules.DataFile import ReadDataFile
from modules.APIToken import GetToken
from modules.Receiver import GetPhoneNumbers
from modules.Variables import ReadArgs, fileData
from modules.TestEventsSMS import TestEvents

print(end="\n")
ReadArgs()
GetToken()
data = ReadDataFile(fileData.dataFileName)
GetPhoneNumbers(data)
CheckForModel(data)
CheckForMobile()
TestEvents(data)
UploadCSV()
print("|---------------FINISHED---------------|")