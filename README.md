# User documentation (in progress)
## Prerequisites
- Installed sshpass utility  
For ubuntu command `sudo apt install sshpass` can be used.
- The device that is being tested should be tested on fresh settings
*It is recommended to create a profile if current devices settings are important.*
- Installed additional python packages:
    - paramiko `pip install paramiko`
    - requests `pip install requests`
## File, Folder structure
- event-report-test.py -> main automatic test program file
- structure.json -> JSON configuration file structure
- event-config.json -> configuration file example for RUTX11 with FW:RUTX_R_00.07.04.2
- classes
    - DeviceData.py -> stores data about device system, hardware information, SIM card numbers
    - 

## Configuration file structure
*explain config file*
## To create and activate virtual environment
Virtual environment is used if it is not wanted to install packages globally
- Install virtualenv `python3 -m pip install virtualenv`
- Create virtual environment `virtualenv -p python3 .venv`
- Execute the activate script `source .venv/bin/activate`
- To deactive virtual environment type `deactivate`
## Launching the automatic test
- Using command python3 launch the main file 'event-report-test.py' `python3 event-report-test.py`
- Using flags, if necessary, provide login data, IP addresses of devices and JSON configuration file's path. Flag -h or --help will show you what each flag does and what it requires.
## Tips and recommendations when creating JSON config file
*tips when making config file*
# Task's information, requirements
## Automate the testing of Events Reporting
The purpose of this automated test is to create a program that will test all Events Reporting rules variations and trigger these rules to check whether information is sent when it happens and if the sent information is correct.

The assignment must be completed using the Python programming language. Use third version of python. The test must be able to test Events Reporting with every device that has mobile capabilities. All Events Reporting Types and subtypes must be tested. You must use API to configure Events Reporting rules.

[API documentation](https://teltonikalt.sharepoint.com/sites/NetworksIoTakademija/SitePages/API.aspx#to-read-api-documentation-upload-it-here).
## Test functionality
The test must have a JSON configuration file that fill hold all Events reporting rules configurations and triggers that will make the device send SMS message or email about it to another device. Configuration file must also contain information what information the received message on certain events reporting rule will contain and from which number it must come. When starting the test, it is necessary to check whether the connected product is the one indicated as being tested.

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