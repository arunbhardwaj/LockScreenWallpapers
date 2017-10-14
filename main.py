'''
Extracts the windows content files used to generate lockscreen wallpapers
Created on Oct 10, 2017

@author: Arun
'''
import shutil, os, sys
from pathlib import Path
from datetime import datetime
import time

if __name__ == '__main__':
    pass

os.chdir('C:\\Users\\Arun\\Desktop\\new_folder')
lastMod = 0.0
sourcedir = Path('C:\\Users\\Arun\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets\\')
destinationdir = Path('C:\\Users\\Arun\\Desktop\\new_folder')
log_file = open('log.txt', 'w')
log_file.write('The folder selected was {}\n'.format(sourcedir))

#Gets the last modified timestamp in regards to date not hours minutes seconds as these values change from file to file despite the modified dates remaining the same
for f in os.listdir(sourcedir):
    file = os.path.join(sourcedir,f)
    fileMod = os.path.getmtime(file)
    if fileMod > lastMod:
        lastMod = fileMod

lastMod = datetime.fromtimestamp(lastMod).strftime('%Y-%m-%d')
lastMod = time.mktime(datetime.strptime(lastMod, '%Y-%m-%d').timetuple())
log_file.write("The last modified file was on: {} aka {}\n".format(datetime.fromtimestamp(lastMod).strftime('%Y-%m-%d %H:%M:%S'), lastMod))

#Compares files to timestamp as well as size to copy the correct files
for f in os.listdir(sourcedir):
    file = os.path.join(sourcedir,f)
    fileMod = os.path.getmtime(file)
    fileSize = os.path.getsize(file)
    if (fileMod >= lastMod) and (fileSize >= 300000) :
        shutil.copy(file, destinationdir)
        log_file.write('{} was copied over.\n'.format(f))
    #log_file.write("{}  {}\n".format(f,fileMod >= lastMod))

#Once copied, the files get renamed to picture files
for f in os.listdir(destinationdir):
    if f.endswith(".txt") or f.endswith(".py") or f.endswith(".jpg"):
        continue
    else:
        try:
            os.rename(os.path.join(destinationdir,f),os.path.join(destinationdir,f+'.jpg'))
        except FileExistsError:
            log_file.write("{} file already exists.\n".format(f))
            os.remove(os.path.join(destinationdir,f))
            
log_file.close()


"""
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