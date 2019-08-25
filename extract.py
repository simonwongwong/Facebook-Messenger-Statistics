import os
import sys
import shutil
from pathlib import Path

"""
This script should be placed in the folder that contains folders with chat names (and chat JSON files within).
Currently as of the latest update (August 2019) the correct folder would be "{extract_location}/messages/inbox"
"""

if __name__ == "__main__":
    try:
        cwd = sys.argv[1]
        dest = sys.argv[2]
    except IndexError:
        cwd = dest = os.getcwd()

    archive = Path(cwd) / "archive"
    root = Path(cwd)
    dir_files = os.listdir(cwd)
    folders = [x for x in dir_files if os.path.isdir(x)]

    if not os.path.exists(archive):
        os.mkdir(archive)

    for folder in folders:
        try:
            if "message_1.json" in os.listdir(folder):
                os.rename((root / folder) / "message_1.json", str(root / (folder + ".json")))

            os.rename(folder, archive / folder)
        except Exception as err:
            print(err)
            print("skipped folder due to error:", folder)
            os.chdir(root)
