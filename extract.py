import os, shutil

media = ".\\media\\"

files = os.listdir()

files = [x for x in files if os.path.isdir(x)]


if not os.path.exists(media):
	os.mkdir(media)

for file in files:
	try:
		os.chdir(file)
		os.rename("message.json", "..\\"+file+".json")
		os.chdir("..")
		shutil.move(file, media+file)
	except:
		os.chdir("..")
		print("skipped", file)

