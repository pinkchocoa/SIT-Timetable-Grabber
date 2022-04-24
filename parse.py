import os, sys
from os.path import expanduser
import fileIo
import datetime
import pandas as pd
from icalendar import Calendar, Event, LocalTimezone
import easygui
from random import randint

fileName = "schedule.csv"
scheduleTxt = "classSchedule.txt"

def parseScheduleTxt(scheduleTxt):
    classCode = ["CSC", "SEM"] #change to a list of class codes avail
    locationCode = ["NYP-", "NP-", "DV-", "RP-", "SP-", "TP-"]
    classTypes = ["Laboratory", "Lecture"] #add all class types
    classNum = ["P1", "P2", "P3", "ALL", "Q1"]
    timeCode = ["AM -", "PM -"]
    newClass = "Class Nbr"
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    currentYear = date.strftime("%Y")

    #read file
    listOfClass = fileIo.fileToList(scheduleTxt)

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
        for y in classCode:
            if y in x:
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
        for y in locationCode:
            if y in x:
                csvString["location"] = x
                profName = True #after location is the professors name
                break
    return csvList

def createCSVFile(data, fileName):
    fileIo.createFile(fileName)
    fileIo.deleteFileContents(fileName)
    fileIo.listToFile(data, fileName)

def parseICSFromCSV(fileName):
    # Start calendar file
    cal = Calendar()
    cal.add('prodid', '-//2021/22 Trimester 3 | Undergraduate | SIT | by pinkchocoa//')
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


csvList = parseScheduleTxt(scheduleTxt)
print("Parsing Text.")
createCSVFile(csvList, fileName)
print("Created CSV.")
#parseICSFromCSV(fileName)
