## @file csvToIcs.py
#
# @brief GUI with instructions to grab timetable from in4sit
#        Copyright 2022, Jodie Moh, All rights reserved.
#
# @author Jodie Moh

from txtToCsv import parseScheduleTxt, createCSVFile
from csvToIcs import parseIcsFromCsv
import easygui

def main():
    message = "Login to 'IN4SIT', click on 'Course Management' > 'My Weekly Schedule' > 'List View'." +\
    "\nFrom there, highlight and copy the entire table(s) inclusive of the table title and save it in a .txt file." +\
    "\nClick on continue once the txt file has been created."
    title = "SIT Time Table Grabber Help Box"
    continueText = "Continue"
    output = easygui.msgbox(message, title, continueText)
    if(output is None):
        return

    message = "Open the .txt file that you have saved."
    output = easygui.msgbox(message, title, continueText)
    if(output is None):
        return

    try:
        data = parseScheduleTxt()
    except Exception as e:
        message = "An error has occured, did you select the right text file?"
        easygui.msgbox(message, title)

    try:
        createCSVFile(data)
    except Exception as e:
        message = "An error has occured, csv file cannot be created. \nPlease ensure that the .txt file used is valid."
        easygui.msgbox(message, title)

    message = "Continue to convert the created .csv file into .ics format."
    output = easygui.buttonbox(message, title, ["Exit", continueText])
    if(output is None or output == "Exit"):
        return
    elif(output == continueText):
        try:
            parseIcsFromCsv()
        except Exception as e:
            message = "An error has occured, ical file cannot be created. \nPlease ensure that the .txt or .csv file used is valid."
            easygui.msgbox(message, title)
    
    message = "Open the .ical file in your calendar application to import!"
    output = easygui.msgbox(message, title, "Bye!")

main()