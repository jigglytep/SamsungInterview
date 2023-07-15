# SamsungInterview

`main.py` Used to kick of the tests

`emails.py` Used to connect to the GMAIL API and download emails from my 'LTsenovoy@gmail.com' email account. Requires `credentials.json` file to be work.

`communications.py` Contains functions called by the databse to mock communications to host machine.

`api.py` Dummy functions called by the application to mimic the described envioronment in the requirement document.

`parseMail.py` Functions that are used to parse data out of subject and body strings of recieved emails.

`sqliteProcess.py` Database functionality, has commented out Trigger definitions and commands that connect to the database, insert data, and open a listening stream to updates from triggers.

`testData.py` Contains a list of test subject and email bodies in the form of text.
