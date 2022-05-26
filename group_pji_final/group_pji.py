import os
import shutil
import sys

# .exe --> sys.executable, .py --> __file__
try:
    if sys.frozen or sys.importers:
        script_directory = os.path.dirname(sys.executable)
except AttributeError:
    script_directory = os.path.dirname(os.path.realpath(__file__))

# creates a backup folder if it doesn't exist
if not os.path.isdir(os.path.join(script_directory, 'Backup')):
    os.mkdir(os.path.join(script_directory, 'Backup'))

# moves all files to backup folder for if anything goes wrong
with os.scandir(script_directory) as it:
    for entry in it:
        if entry.name.endswith('html') and entry.is_file():
            try:
                shutil.copy2(entry.path, os.path.join(script_directory, 'Backup'))
            except:
                print("An exception occurred")

# goes through all files and moves them to pji folder if folder exists, if file with same name already exists it removes
# the source file
# creates new directory if pji folder isn't found, then moves the files in it
with os.scandir(script_directory) as it:
    for entry in it:
        if entry.name.endswith('html') and entry.is_file():
            htmlPji = entry.name[0:7]  # pji
            htmlPath = entry.path  # path pji
            if os.path.isdir(os.path.join(script_directory, htmlPji)):
                try:
                    shutil.move(htmlPath, os.path.join(script_directory, htmlPji))
                except:
                    os.remove(htmlPath)
            elif not os.path.isdir(os.path.join(script_directory, htmlPji)):
                os.mkdir(os.path.join(script_directory, htmlPji))
                shutil.move(htmlPath, os.path.join(script_directory, htmlPji))
            else:
                print("Something wrong happened while moving files")
