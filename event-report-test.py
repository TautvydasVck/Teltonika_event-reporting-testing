# imports
import json
from getpass import getpass
from tkinter.filedialog import askopenfilename

# main function with user login
def Main():
    print("Enter router's admin page credentials")
    print("Username: ", end="")
    name = input()
    pswd = getpass()
    jsonFile = GetConfigFile()
    #ReadEvents(jsonFile)
    with open(jsonFile) as f:
        data = json.load(f)
    # print("value: {}".format(jsonFile))
    
def LoginToDevice(data):
    ip = data["info"]["ip-address"]

def GetConfigFile():
    return askopenfilename()
    # return print("File is in: {}".format(fileLocation))

def CheckForMobile(ip, data):    
    #device's info
    model=data["info"]["product"]    

#def ReadEvents(file):
#    data = json.dumps(file)
    

Main()
