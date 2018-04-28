import os, shutil

archive = ".\\archive\\"

files = os.listdir()

stickerIndex = files.index("stickers_used")
del files[stickerIndex]

shutil.move("stickers_used", archive)

files = [x for x in files if not ".py" in x]


if not os.path.exists(archive):
	os.mkdir(archive)

for file in files:
	os.chdir(file)
	try:
		os.rename("message.json", "..\\"+file+".json")
	except:
		print("skipped", file)
	os.chdir("..")
	shutil.move(file, archive+file)


