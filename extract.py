import os
import shutil
from pathlib import Path

"""
This script should be placed in the folder that contains folders with chat names (and chat JSON files within).
Currently as of December 2018 the correct folder would be "{extract_location}/messages/inbox"
"""

archive = Path(os.getcwd()) / "archive"
root = Path(os.getcwd())

files = os.listdir()

# for backwards compatability with older facebook extracts
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
		if "message.json" in os.listdir():
			os.rename("message.json", str(root / (file + ".json")))
		os.chdir("..")
		os.mkdir(archive / file)
		os.rename(file, archive / file)
	except:
		print("skipped folder due to error:", file)
		os.chdir(root)
