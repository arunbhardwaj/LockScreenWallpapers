'''
A script for extracting the windows content files used to generate lockscreen wallpapers.
Created on Oct 10, 2017

@author: Arun
'''
import shutil, os, getpass, time
from pathlib import Path
from datetime import datetime

#Returns the last modified timestamp in regards to date not hours/minutes/seconds as these values change from file to file despite the modified dates remaining the same
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
    os.chdir(destinationdir)
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

    
