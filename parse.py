import os, sys
import fileIo
import datetime
from os.path import expanduser, isdir
import easygui

def parseScheduleTxt():
    start_dir = '~/'
    if isdir(expanduser("~/Desktop")):
        start_dir = '~/Desktop/'
    msg = 'Please select the .txt file to be converted to .csv'
    scheduleTxt = easygui.fileopenbox(msg=msg, title="", default=expanduser(start_dir), filetypes=["*.txt"])

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

def createCSVFile(data):
    # Write final .ics file to same directory as input file.
    fileName = easygui.filesavebox(msg='Save .csv File', title='', default=expanduser('~/') + 'calendar.csv', filetypes=['*.csv'])
    if(fileName is not None):
        with open(fileName, "w", encoding="utf-8") as f:
            for l in data:
                f.write(l+"\n")

createCSVFile(parseScheduleTxt())
