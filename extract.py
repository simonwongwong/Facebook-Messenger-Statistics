import os, shutil

files = os.listdir()

stickerIndex = files.index("stickers_used")
del files[stickerIndex]

os.remove("messages.html")
shutil.move("stickers_used", archive)

files = [x for x in files if not ".py" in x]
files = [x for x in files if not ".html" in x]

archive = "..\\archive\\"

if not os.path.exists(archive):
	os.mkdir(archive)

for file in files:
	os.chdir(file)
	try:
		os.rename("message.html", "..\\"+file+".html")
	except:
		print("skipped", file)
	os.chdir("..")
	shutil.move(file, archive+file)


