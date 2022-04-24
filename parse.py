import os, sys
import fileIo
import datetime
import pandas as pd
from icalendar import Calendar, Event, LocalTimezone
import easygui
from random import randint

fileName = "schedule.csv"
scheduleTxt = "classSchedule.txt"

def parseScheduleTxt(scheduleTxt):
    classCode = "CSC" #change to a list of class codes avail
    locationCode = "NYP" #change to a list of SIT campus locations
    classTypes = ["Laboratory", "Lecture"] #add all class types
    classNum = ["P1", "P2", "P3", "ALL", "Q1"]
    timeCode = ["AM -", "PM -"]
    newClass = "Class Nbr"
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    currentYear = date.strftime("%Y")

    #read file
    listOfClass = fileIo.file_to_list(scheduleTxt)

    csvList = ["Subject,Start Date,Start Time,End Date,End Time,Location,Description"]
    # Subject - class name + type
    # Start Date - MM/DD/YYYY
    # Start Time - 24 hour format (13:45) or 12 AM/PM (01:45 PM)
    # End Date
    # End Time
    # Location
    # Description

    #As of Python version 3.7, dictionaries are ordered. 
    #In Python 3.6 and earlier, dictionaries are unordered.
    csvString = {
        "subject" : "NA",
        "startDate" : "NA",
        "startTime" : "NA",
        "endDate" : "NA",
        "endTime" : "NA",
        "location" : "NA",
        "description" : "NA"
    }

    def appendToCSVList():
        temp = ""
        for x in csvString.values():
            temp += x
            temp += ","
        csvList.append(temp[:-1]) #remove last comma

    def clearDict(clearAll):
        for x in csvString.keys():
            if(not clearAll and x == "subject"):
                continue
            csvString[x] = "NA"

    def changeDateFormat(date):
        #change from DD/MM/YYY to MM/DD/YYYY
        date = date.split("/")
        newDate = date[1] + "/" + date[0] + "/" + date[2]
        return newDate

    profName = False

    for x in listOfClass:
        if(x.strip() == ""):
            continue
        if classCode in x:
            module = x
            continue
        for y in classTypes:
            if y in x:
                csvString["subject"] = csvString["subject"][:-1]
                csvString["subject"] += " " + y + ")"
                continue
        for y in timeCode:
            if y in x:
                timeSplit = x.split(" ")
                csvString["startTime"] = timeSplit[1]
                csvString["endTime"] = timeSplit[3]
                continue
        for y in classNum:
            if y in x:
                csvString["subject"] = module + " ("
                csvString["subject"] += x + ")"
                continue
        if locationCode in x:
            csvString["location"] = x
            profName = True #after location is the professors name
            continue
        if currentYear in x:
            dateSplit = x.split(" ")
            csvString["startDate"] = changeDateFormat(dateSplit[0])
            csvString["endDate"] = changeDateFormat(dateSplit[2])
            profName = False
            appendToCSVList()
            #clear dictionary
            clearDict(False)
        if(profName):
            if("Professor" in csvString["description"]):
                csvString["description"] += " "
                csvString["description"] += x.replace(",","")
            else:
                csvString["description"] = "Professor(s): "
                csvString["description"] += x.replace(",","")
            continue
    return csvList


def createCSVFile(data, fileName):
    fileIo.create_file(fileName)
    fileIo.delete_file_contents(fileName)
    fileIo.list_to_file(data, fileName)



csvList = parseScheduleTxt(scheduleTxt)
print("conversion completed")
createCSVFile(csvList, fileName)
print("csv created")


colNames = ["Subject,Start Date,Start Time,End Date,End Time,Location,Description"]
df = pd.read_csv(fileName, names=colNames)
for index, row in df.iterrows():
    print(row['Subject'])

# # Start calendar file
# cal = Calendar()
# cal.add('prodid', '-//2021/22 Trimester 3 | Undergraduate | SIT//')
# cal.add('version', '2.0')

# event = Event()
# event.add('description', row['Description'])

# event = Event()
# event.add('summary', 'Python meeting about calendaring')
# event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=UTC))
# event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=UTC))
# event.add('description', row['Description'])
# event.add('location', row['Location'])
# event.add('dtstamp', datetime.replace( datetime.now(), tzinfo=LocalTimezone() ))
# event['uid'] = str(randint(1,10**30)) + datetime.now().strftime('%Y%m%dT%H%M%S') + '___n8henrie.com'

# cal.add_component(event)
# # Write final .ics file to same directory as input file.
# f = open(easygui.filesavebox(msg='Save .ics File', title='', default=expanduser('~/') + 'calendar.ics', filetypes=['*.ics']), 'wb')
# f.write(cal.to_ical())
# f.close()