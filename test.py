from modules.ResultFile import UploadCSV
from modules.PrimaryChecks import CheckForMobile, CheckForModel
from modules.DataFile import GetConfigData
from modules.APIToken import GetToken
from modules.Receiver import GetPhoneNumbers
from modules.Variables import ReadArgs, fileData
from modules.TestEvents import TestEvents
from classes.Utilities import Text

print(end="\n")
ReadArgs()
GetToken()
data = GetConfigData(fileData.dataFileName)
GetPhoneNumbers(data)
CheckForModel(data)
CheckForMobile()
TestEvents(data)
UploadCSV()
print(Text.Purple("|---FINISHED---|"))