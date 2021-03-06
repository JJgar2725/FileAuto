# imported modules
import os
import shutil
import sys
import time
import logging
import pathlib
import datetime
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# loads in path from .env file
load_dotenv()

# function to handle name error checking before moving file
def moveDir(item, path, itemname, itemext):
    # if no error
    try:
        shutil.move(item, path)
    
    # if shutil.Error comes up, rename and move
    except shutil.Error:
        dt = str(datetime.datetime.now().second)
        newname = itemname + '_' + dt + itemext
        os.rename(item, newname)
        shutil.move(newname, path)

# set current working directory to Downloads folder
os.chdir(os.environ['PATH_TO_DOWNLOADS'])

# class for file handling
class FileHandler(FileSystemEventHandler):
    # when Downloads folder is modified
    def on_modified(self, event):
        
        # wait time in order to let file somewhat download
        time.sleep(5)

        # if directories don't exist, create them
        pathlib.Path('PDF\'s').mkdir(parents=True, exist_ok=True)
        pathlib.Path('Images').mkdir(parents=True, exist_ok=True)
        pathlib.Path('EXE\'s').mkdir(parents=True, exist_ok=True)
        pathlib.Path('Misc').mkdir(parents=True, exist_ok=True)
        pathlib.Path('ZIP\'s').mkdir(parents=True, exist_ok=True)

        # directories to each folder in Downloads
        pdfdir = str(os.path.abspath("PDF's"))
        imgdir = str(os.path.abspath("Images"))
        exedir = str(os.path.abspath("EXE's"))
        miscdir = str(os.path.abspath("Misc"))
        zipdir = str(os.path.abspath("ZIP's"))

        # get a list of current files in directory
        items = os.listdir()

        # create lists for file name and extensions
        filenames = []
        filexts = []

        # remove pdfs, imgs, exes, and misc out of list
        try:
            items.remove("PDF's")
            items.remove("EXE's")
            items.remove("Misc")
            items.remove("Images")
            items.remove("ZIP's")
        except ValueError:
            pass

        # splits filenames and file extensions into seperate lists
        for x in range(len(items)):
            filename, fileexts = os.path.splitext(items[x])
            filenames.append(filename)
            filexts.append(fileexts)

        # splits each file type into different lists
        for x in range(len(items)):
            if filexts[x] == '.pdf' or filexts[x] == '.doc' or filexts[x] == '.docx':
                moveDir(items[x], pdfdir, filenames[x], filexts[x])

            elif filexts[x] == '.jpg' or filexts[x] == '.png' or filexts[x] == '.jpeg':
                moveDir(items[x], imgdir, filenames[x], filexts[x])

            elif filexts[x] == '.exe':
                moveDir(items[x], exedir, filenames[x], filexts[x])

            elif filexts[x] == '.zip':
                moveDir(items[x], zipdir, filenames[x], filexts[x])

            elif filexts[x] == '':
                moveDir(items[x], miscdir, filenames[x], filexts[x])
            
            else:
                moveDir(items[x], miscdir, filenames[x], filexts[x])


# path to Downloads folder
path = os.environ['PATH_TO_DOWNLOADS']

# create an object of FileHandler class
event_handler = FileHandler()

# create an object of Observer class
observer = Observer()

# schedule observer object recursively and starts
observer.schedule(event_handler, path, recursive=True)
observer.start()

# will run every second until KeyboardInterrupt
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
