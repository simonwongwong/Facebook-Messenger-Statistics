import os, shutil

archive = ".\\archive\\"

files = os.listdir()

try:
	stickerIndex = files.index("stickers_used")
	del files[stickerIndex]
	shutil.move("stickers_used", archive)

files = [x for x in files if not ".py" in x]


if not os.path.exists(archive):
	os.mkdir(archive)

for file in files:
	try:
		os.chdir(file)
		os.rename("message.json", "..\\"+file+".json")
		os.chdir("..")
		shutil.move(file, archive+file)
	except:
		print("skipped", file)



