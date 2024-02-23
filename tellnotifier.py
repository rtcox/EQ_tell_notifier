'''
Required python libraries:
-os
-re
-plyer
-time

library install example:
python -m pip install plyer

To run script:
-edit the logfile variable in this file with the path to your character log file
-python /path/to/script/tellnotifier.py
'''

import os
import re
import time
from plyer import notification


######VARIABLES######
#everquest character log file to follow
logfile = r'C:\TAKP\eqlog_Moscow_pq.proj.txt'
#####################

def follow(thefile):
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)

    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue

        yield line

def grab_content(line, delim):
    linesplit = re.split(delim, line)
    return linesplit

def desktop_notify(character, message):
    title = "Tell From: "+character
    notification.notify(
        title=title,
        message=message,
        timeout=15  # Display duration in seconds
        )

def livefollow(delim):
    eqlogfile = open(logfile, "r+")
    loglines = follow(eqlogfile)
    for line in loglines:
        if delim in line:
            line = re.split(r'] ', line)[1]
            line = line.strip()
            line = line[:-1]
            line_content = grab_content(line, delim)
            if len(line_content) == 2:
                character = line_content[0]
                message = line_content[1]
                print("Tell Recieved from "+character+": "+line)
                desktop_notify(character, message)


delim = 'tells you, \''
print("Watching "+logfile+"...")
print("Waiting for tells...")
livefollow(delim)
