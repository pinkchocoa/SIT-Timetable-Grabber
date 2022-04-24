## @file fileIo.py
#
# @brief this file contains the general functions used for filo i/o purposes
#
# @author Jodie
#
# @section libraries_main Libraries/Modules
# - os standard library
#   - required to create files and/or directories

# Imports
import os

def createProjDir(directory):
    """! This method creates a directory with the user input
    @param directory directory path
    """
    if not os.path.exists(directory):
        #print('Creating directory ' + directory)
        os.makedirs(directory)

def createFile(path):
    """! This method creates a file with the user input
    @param path file path
    """
    if not os.path.isfile(path):
        writeFile(path, '')
        #print("file created")

# Create a new file
def writeFile(path, data):
    """! This method writes to a file with the user input
    @param path file path
    @param data data to be written to the file
    """
    with open(path, 'w', encoding="utf-8") as f: # 'w' for write
        f.write(data)


# Add data onto an existing file
def appendToFile(path, data):
    """! This method writes to an existing file with the user input
    @param path file path
    @param data data to be written to the file
    """
    with open(path, 'a', encoding="utf-8") as file: # 'a' for append
        file.write(data + '\n')


# Delete the contents of a file
def deleteFileContents(path):
    """! This method deletes the contents of a file
    @param path file path
    """
    if  os.path.isfile(path):
        open(path, 'w', encoding="utf-8").close()


# Read a file and convert each line to items
def fileToList(file_name):
    """! This method reads a file and convert each line to items
    @param file_name file name
    @return list with the file data
    """
    results = list()
    with open(file_name, 'rt', encoding="utf-8") as f:
        for line in f:
            results.append(line.replace('\n', '')) # remove new line character
    return results


# Iterate through a list, each item will be a line in a file
def listToFile(data, file_name):
    """! This method iterate through a list, each item will be a line in a file
    @param data data to be entered into the file
    @param file_name file name
    """
    with open(file_name, "w", encoding="utf-8") as f: #added encoding for UnicodeEncodeError 
        for l in data:
            f.write(l+"\n")