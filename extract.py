import os
import shutil

"""
This script should be placed in the folder that contains folders with chat names (and chat JSON files within).
Currently as of December 12, 2018 the correct folder would be "{extract_location}/messages/inbox"
"""

archive = ".\\archive\\"

files = os.listdir()

try:
    sticker_folder = files.index("stickers_used")
    del files[sticker_folder]
    shutil.move("stickers_used", archive)
except:
    pass

files = [x for x in files if os.path.isdir(x)]


if not os.path.exists(archive):
    os.mkdir(archive)

for file in files:
    try:
        os.chdir(file)
        os.rename("message.json", "..\\" + file + ".json")
        os.chdir("..")
        shutil.move(file, archive + file)
    except:
        print("skipped", file)
