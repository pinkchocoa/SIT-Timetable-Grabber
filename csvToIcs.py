from os.path import expanduser, isdir
import datetime
import pandas as pd
from icalendar import Calendar, Event, LocalTimezone
import easygui
from random import randint

#CSV must have the following headers in the exact format
# Subject
# Start Date - MM/DD/YYYY
# Start Time - 12 AM/PM (01:45 PM)
# End Date - MM/DD/YYYY
# End Time - 12 AM/PM (01:45 PM)
# Location
# Description

def parseICSFromCSV():
    start_dir = '~/'
    if isdir(expanduser("~/Desktop")):
        start_dir = '~/Desktop/'
    msg = 'Please select the .csv file to be converted to .ics'
    fileName = easygui.fileopenbox(msg=msg, title="", default=expanduser(start_dir), filetypes=["*.csv"])

    # Start calendar file
    cal = Calendar()
    cal.add('prodid', '-//ical conversion by pinkchocoa//')
    cal.add('version', '2.0')

    df = pd.read_csv(fileName)
    for index, row in df.iterrows():
        event = Event()
        event.add('summary', row["Subject"])

        timeStamp = row["Start Date"] + " " + row["Start Time"]
        timeStamp = datetime.datetime.strptime(timeStamp, "%m/%d/%Y %I:%M%p")
        event.add('dtstart', timeStamp)
        timeStamp = row["End Date"] + " " + row["End Time"]
        timeStamp = datetime.datetime.strptime(timeStamp, "%m/%d/%Y %I:%M%p")
        event.add('dtend', timeStamp)

        event.add('description', row['Description'])
        event.add('location', row['Location'])
        event.add('dtstamp', datetime.datetime.replace( datetime.datetime.now(), tzinfo=LocalTimezone() ))
        event['uid'] = str(randint(1,10**30)) + datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

        cal.add_component(event)

    # Write final .ics file to same directory as input file.
    f = open(easygui.filesavebox(msg='Save .ics File', title='', default=expanduser('~/') + 'calendar.ics', filetypes=['*.ics']), 'wb')
    f.write(cal.to_ical())
    f.close()

parseICSFromCSV()