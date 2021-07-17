from os import path, walk
import os
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

defaultdir = "/home/gavin/Python/Flask Projects/ChromeProfiles/Profiles/MacChromeProfiles"
# defaultdir = "/home/gavin/Python/Flask Projects/ChromeProfiles/Profiles/WinChromeProfiles"

def launch(dirname="Jessie2"):
    print('reached zip_directory()')
    dirpath = path.join(defaultdir, dirname)
    if not path.isdir(dirpath):
        print({"message": "No profile dirs exist called: {dirname}"})
        
    with ZipFile(f"{dirpath}.zip", "w", ZIP_DEFLATED) as zip_obj:
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                zip_obj.write(path.join(root, file), 
                              path.relpath(path.join(root, file), 
                              path.join(path, '..')))

        
      
    print('Success!')

def sh_method(dirname="Jessie2"):
    dirpath = path.join(defaultdir, dirname)
    shutil.make_archive(f"{dirpath}", 'zip', dirpath)

if __name__ == "__main__":
    sh_method()