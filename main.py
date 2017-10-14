'''
A script for extracting the windows content files used to generate lockscreen wallpapers.
Created on Oct 10, 2017

@author: Arun
'''
import shutil, os, getpass, time
from pathlib import Path
from datetime import datetime

#Returns the last modified timestamp in regards to date not hours minutes seconds as these values change from file to file despite the modified dates remaining the same
def lastModifiedFile(sourceDirectory):
    lastMod = 0.0
    for f in os.listdir(sourceDirectory):
        file = os.path.join(sourceDirectory,f)
        fileMod = os.path.getmtime(file)
        if fileMod > lastMod:
            lastMod = fileMod
    return lastMod

#Compares files to timestamp as well as size to copy the correct files
def copy(sourceDirectory, destinationDirectory, sortingDate, logFile=None):
    marker = True
    for f in os.listdir(sourceDirectory):
        file = os.path.join(sourceDirectory,f)
        fileMod = os.path.getmtime(file)
        fileSize = os.path.getsize(file)
        if (fileMod >= sortingDate) and (fileSize >= 300000):
            shutil.copy(file, destinationDirectory)
            try: 
                logFile.write('{} was copied over.\n'.format(f))
            except AttributeError:
                if marker == True:
                    print("No log file was specified.\n")
                    marker = False
            
#Once copied, the files get renamed to picture files
def convertToJPG(directory, logFile=None):
    marker = True
    for f in os.listdir(directory):
        if f.endswith(".txt") or f.endswith(".py") or f.endswith(".jpg"): #or f.isfile() == False:
            continue
        else:
            try:
                os.rename(os.path.join(directory,f),os.path.join(directory,f+'.jpg'))
            except FileExistsError:
                os.remove(os.path.join(directory,f))
                try:
                    logFile.write("{} file already exists.\n".format(f))
                except AttributeError:
                    if marker == True:
                        print("No log file was specified.\n")
                        marker = False

#Verifies that the file_path exists and, if not, creates it.
def checkDirectory(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        
def main():
    username = getpass.getuser()
    sourcedir = Path('C:\\Users\\{}\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets\\'.format(username))
    destinationdir = Path('C:\\Users\\{}\\Desktop\\new_folder'.format(username))
    checkDirectory(destinationdir)
    os.chdir('C:\\Users\\{}\\Desktop\\new_folder'.format(username))
    lastMod = 0.0
    log_file = open('log.txt', 'w')
    log_file.write('The folder selected was {}\n'.format(sourcedir))
    lastMod = lastModifiedFile(sourcedir)
    lastMod = datetime.fromtimestamp(lastMod).strftime('%Y-%m-%d')
    lastMod = time.mktime(datetime.strptime(lastMod, '%Y-%m-%d').timetuple())
    log_file.write("The last modified file was on: {} aka {}\n".format(datetime.fromtimestamp(lastMod).strftime('%Y-%m-%d %H:%M:%S'), lastMod))
    copy(sourcedir, destinationdir, lastMod, log_file)
    convertToJPG(destinationdir, log_file)
    log_file.close()
    
if __name__ == '__main__':
    main()

"""
********************************************
* method 2: works but less module-friendly *
********************************************
for f in os.listdir(sourcedir):
    file = os.path.join(sourcedir,f)
    fileMod = os.path.getmtime(file)
    fileSize = os.path.getsize(file)
    if (fileMod >= lastMod) and (fileSize >= 300000) :
        shutil.copy(file, destinationdir)
        log_file.write('{} was copied over.\n'.format(f))
    #log_file.write("{}  {}\n".format(f,fileMod >= lastMod))
    
for f in os.listdir(destinationdir):
    if f.endswith(".txt") or f.endswith(".py") or f.endswith(".jpg"):
        continue
    else:
        try:
            os.rename(os.path.join(destinationdir,f),os.path.join(destinationdir,f+'.jpg'))
        except FileExistsError:
            log_file.write("{} file already exists.\n".format(f))
            os.remove(os.path.join(destinationdir,f))

*********************
* method 1 (failed) *
*********************
for folderName, fileNames in os.walk(directory):
    log_file.write('The folder selected was ' + folderName)
    for fileName in fileNames:
        if (os.path.getmtime(fileName) > lastMod):
            lastMod = os.path.getmtime(fileName)
            continue
        if (os.path.getsize(fileName) >= 300) and (os.path.getmtime(fileName) == lastMod):
            shutil.copy('' + fileName,'C:\\Users\\Arun\\Desktop\\new_folder')
            log_file.write('{} was copied over'.format(fileName))



directory = os.fsencode('C:\\Users\\Arun\\Desktop\\new_folder')
for file in os.listdir(directory):
    fileName = os.fsdecode(file)
    if fileName.endswith(".txt") or fileName.endswith(".py"):
        continue
    else:
        fileName.append(".jpg")
"""

#file_list = [f for f in destinationdir.glob('**/*') if f.is_file()]