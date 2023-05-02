# Documentation
## Prerequisites
- Installed sshpass utility.  
For ubuntu command `sudo apt install sshpass` can be used.
- The device that is being tested should be tested on fresh settings.  
It is recommended to create a profile if current device settings are important.
- Installed additional python packages (with dependencies):
    - paramiko `pip install paramiko`
    - requests `pip install requests`
## Launching the automatic test
- Using python3 launch the main file `python3 event-report-test.py`.
- Using flags, if necessary, provide login data, IP addresses of devices and JSON configuration file's path. Flag `-h` or `--help` will show you what each flag means and what it requires.
## JSON configuration file structure
![JSON structure](/structureExplained.png)

One object in `events-triggers` list is one type of event (and its subtypes) `event-data{}` with corresponding triggers `trigger-data{}`.
### About event report data
- There must be a message for each event subtype.
- Since event reporting with email is not tested `"email-config"` part can be an empty object `"email-config":{}` or simply omitted.
- Event report message can be multiline (can have `\n` inside string).
- Event report message can have device's (that is being tested) IMEI. Type `%ie` inside string.
### About trigger data
- There must be a trigger for each event subtype.
- Each trigger can have multiple steps (a list of steps).
- `"wait-time":""` is time in seconds for program to pause before continuing to the next step or a next trigger.
- After each complete trigger (**not** each trigger's step) a 10 second delay is automatically added before SMS content is checked.
- If you need to retrieve API token after a trigger in order to continue the test set `"retrieve-token":"1"`. If you do not want to retrieve the token leave as is `"retrieve-token":""`.
- Trigger step can **only** be api/ssh/cmd/ubus.
- Trigger step type api:
    - Sends data to device via API.
    - **Required data**: method (can **only** be put/post), api-path and api-body. 
    - **Additional data**: wait-time and retrieve token.
    - Example: 
    ```    
    {
      "type": "api",
      "command": "",
      "wait-time": "",
      "method": "post",
      "api-path": "/network/mobile/operator_lists/config",
      "api-body": {
        "data": {
          "name": "test"
        }
      },
      "retrieve-token": ""
    }   
    ```
- Trigger step type ssh:
    - Sends a standard command to device via SSH.
    - **Required data**: command. 
    - **Additional data**: wait-time and retrieve token.
    - Example: 
    ```
    {
      "type": "ssh",
      "command": "reboot -p",
      "wait-time": "120",
      "method": "",
      "api-path": "",
      "api-body": {},
      "retrieve-token": "1"
    }          
    ```
- Trigger step type cmd:
    - Writes a command in pc's (the one that is being used) terminal.
    - **Required data**: command. 
    - **Additional data**: wait-time and retrieve token.
    - Example: 
    ```
    {
      "type": "cmd",
      "command": "sshpass -p 1324 ssh root@192.168.1.1 -o ExitOnForwardFailure='yes'",
      "method": "",
      "api-path": "",
      "api-body": {},
      "retrieve-token": "",
      "wait-time": ""
    }
    ```
- Trigger step type: ubus:
    - Sends an UBUS command to device via SSH.
    - **Required data**: command.
    - **Additional data**: wait-time and retrieve token.
    - Every command **must** end with `\"ubus_rpc_session\":\"\"}'`. Because the program adds a token at the end of the command.
    - Quotes `"` inside string must be escaped `\"`. If not the program might stop during primary checks.
    - Example: 
    ```
    {
      "type": "ubus",
      "command": "ubus call uci set '{\"config\":\"frr\", \"section\":\"bgp\", \"values\":{\"enabled\":true}, \"ubus_rpc_session\":\"\"}'",
      "wait-time": "",
      "method": "",
      "api-path": "",
      "api-body": {},
      "retrieve-token": ""
    }
    ```
## Tips and recommendations when creating JSON configuration file
### Creating event data
To quickly get all event types and subtypes you can send a GET request to device's API endpoint `/api/services/events_reporting/options`. *To use this endpoint provide Bearer token in header.*
### Creating triggers
- An example of test configuration can be found in [event-config.json](/event-config.json) file. That file is created for RUTX11 with FW: RUTX_R_00.07.04.2. When creating triggers for another device with same FW you can reuse most (maybe even all) of the triggers from the example file.
- If trigger is a restart always set `wait-time`. If not than a trigger will be sent when the device is restarting and the test will fail. Also always set `retrieve-token:"1"`. If not than after the restart test will continue with wrong old API token and following API requests will fail.
- If durring a trigger there is some sort of a network restart it is recommended to set `wait-time`. If not than a trigger will be sent when network interface is not ready and the test will fail.
- If a package is needed to trigger the event. Than use an API request to install. It is recommended to set `wait-time`.
## To create and activate virtual environment
Virtual environment is used if it is not wanted to install packages globally.
- Install virtualenv `python3 -m pip install virtualenv`
- Create virtual environment `virtualenv -p python3 .venv`
- Execute the activate script `source .venv/bin/activate`
- To deactive virtual environment type `deactivate`
## Files, Folders structure
- [**event-report-test.py**](event-report-test.py) -> main program file
- [**structure.json**](structure.json) -> JSON configuration file structure
- [**event-config.json**](event-config.json) -> configuration file example for RUTX11 with FW: RUTX_R_00.07.04.2
- **classes**
    - [**DeviceData.py**](/classes/DeviceData.py) -> stores data about device system, hardware information, SIM card numbers.
    - [**EventResultsData.py**](/classes/EventResultData.py) -> stores data about event that is being tested.
    - [**Files.py**](/classes/Files.py) -> stores data about configuration file's, result file's location/name.
    - [**RequestData.py**](/classes/RequestData.py) -> stores data about device connection settings (ip, token, login name, login password).
    - [**TestResultData.py**](/classes/TestResultData.py) -> stores data about whole test results (total events, passed/failed count, test start time).
    - [**Utilities.py**](/classes/Utilities.py) -> used for changing text format (changing color, underline).
- **modules**
    - [**APIToken.py**](/modules/APIToken.py) -> get and store ubuc rpc session token from device that is being tested
    - [**DataFile.py**](/modules/DataFile.py) -> load configuration file.
    - [**FTPConnection.py**](/modules/FTPConnection.py) -> create FTP connection to upload csv result file.
    - [**MessageDecode.py**](/modules/MessageDecode.py) -> decode sender's imei (if there is one in the event report message)
    - [**PrimaryChecks.py**](/modules/PrimaryChecks.py) -> make primary checks before the actual testing starts. Checks if the device (that is being tested) has mobile functionalities, gets sim card phone number/-s. Checks if the model in configuration file matches actual device model. Checks if event subtypes, triggers and messages count matches. Checks if it can be connected to receiver via SSH. Checks if device (that is being tested) can send SMS messages and receive them.
    - [**Receiver.py**](/modules/Receiver.py) -> check what a second device received from event reporting (the device that is being tested) and tell if SMS message is the same and if it was received from correct phone number. Also get amount of received messages and there indexes
    - [**Requests.py**](/modules/Requests.py) -> send event reporting data via API and trigger data via API and/or SSH. Also get device hardware, software information via API.
    - [**Resets.py**](/modules/Resets.py) -> delete all old SMS messages and prepare for next event testing (resets event, that was tested, results and deletes event report, that was created)
    - [**ResultFile.py**](/modules/ResultFile.py) -> create, update and upload csv result file.
    - [**SSHConnection.py**](/modules/SSHConnection.py) -> create SSH connection with device.
    - ~~[**TestEventsMail.py**](/modules/TestEventsEmail.py) -> currently not used.~~
    - [**TestEventsSMS.py**](/modules/TestEventsSMS.py) -> test event reporting with SMS messages (main file for event testing but not main program file).
    - [**Triggering.py**](/modules/Triggering.py) -> handle 4 different kind of triggers (API, SSH, CMD, UBUS).
    - [**Variables.py**](/modules/Variables.py) -> read and store arguments provided on program start.
# Task's information, requirements (temporary)
## Automate the testing of Events Reporting
The purpose of this automated test is to create a program that will test all Events Reporting rules variations and trigger these rules to check whether information is sent when it happens and if the sent information is correct.

The assignment must be completed using the Python programming language. Use third version of python. The test must be able to test Events Reporting with every device that has mobile capabilities. All Events Reporting Types and subtypes must be tested. You must use API to configure Events Reporting rules.

[API documentation](https://teltonikalt.sharepoint.com/sites/NetworksIoTakademija/SitePages/API.aspx#to-read-api-documentation-upload-it-here).
## Test functionality
The test must have a JSON configuration file that fill hold all Events reporting rules configurations and triggers that will make the device send SMS message about it to another device. Configuration file must also contain information what information the received message on certain events reporting rule will contain and from which number it must come. When starting the test, it is necessary to check whether the connected product is the one indicated as being tested.

When the other device receives SMS message about the event it is needed to check the content and sender of the SMS message.

The test results of all events reporting configurations must be stored in a CSV file. Each test writes to a new file. The file name must consist of the product name and the date and time the test was performed. The file itself must contain information about event, message payload that was expected, what payload it received, what number it was supposed to be sent from, what number you got it from, and whether it passed the test.

The following information must be visible in the terminal during testing:
- what product is being tested
- what Event type is being tested
- what Event subtype is being tested
- how many successfully passed the test
- how many failed the test
- how many total configurations are there for testing

The number of successfully and unsuccessfully tested commands should be marked with different colors.
## Documentation
The test must have clear documentation, which will provide Python library dependencies, configuration file examples, and instructions on how to use the test itself. Since the test source code will be hosted on github or another git system, the documentation should be described in [Markdown syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
## Technical requirements for the test
The test must have a clear module structure, where the modules are divided according to the functions they perform. For example the functionality of writing results to a file will be in one module, configuring Events Reporting Rules in another module, etc.

Consider using method chaining where it is suitable.

It is advisable to use dependency injection between modules. It is not necessary to use it everywhere.

Methods must be clear and specific. A single method does not have to perform the actions of the entire program. Split the code into separate methods according to their purpose.

Think about the places where the program can break and make error management so that the program does not break unexpectedly. A try and except block can help.

All parameters that will be passed to the program as arguments at startup must be described as flags.
