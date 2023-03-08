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
    ReadEvents(jsonFile)
    # print("value: {}".format(jsonFile))


def GetConfigFile():
    return askopenfilename()
    # return print("File is in: {}".format(fileLocation))

def ReadEvents(file):
    data = json.dumps(file)
    

Main()
