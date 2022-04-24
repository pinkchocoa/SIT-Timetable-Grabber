import os, sys
import fileIo
import datetime

fileName = "schedule.csv"
scheduleTxt = "classSchedule.txt"

classCode = "CSC" #change to a list of class codes avail
locationCode = "NYP" #change to a list of SIT campus locations
classTypes = ["Laboratory", "Lecture"] #add all class types
timeCode = ["AM", "PM"]
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
currentYear = date.strftime("%Y")

listOfClass = fileIo.file_to_list(scheduleTxt)

# Subject - class name + type
# Start Date - MM/DD/YYYY
# Start Time - 24 hour format (13:45) or 12 AM/PM (01:45 PM)
# End Date
# End Time
# Location
# Description
subject= ""
startDate = ""
startTime = ""
endDate = ""
endTime = ""
location = ""
description = ""

def changeDateFormat(date):
    #change from DD/MM/YYY to MM/DD/YYYY
    date = date.split("/")
    newDate = date[1] + "/" + date[0] + "/" + date[2]

for x in listOfClass:
    if classCode in x:
        module = x
        continue
    for y in classTypes:
        if y in x:
            subject = module + " (" +  y + ")"
            continue
    for z in timeCode:
        if z in x:
            timeSplit = x.split(" ")
            startTime = timeSplit[1]
            endTime = timeSplit[3]
            continue
    if locationCode in x:
        location = x
        continue
    if currentYear in x:
        dateSplit = x.split(" ")
        print(dateSplit)
        startDate = changeDateFormat(dateSplit[0])
        endDate = changeDateFormat(dateSplit[2])
        print(startDate)
        print(endDate)
        




def createCSVFile(fileName):
    fileIo.create_file(os.path.join(os.getcwd(), filename))
