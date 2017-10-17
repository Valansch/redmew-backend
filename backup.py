#!/usr/bin/python

import time
from shutil import copyfile
import os

mtime = 0
count = 0
path = "/home/factorio/server/_autosave1.zip"
backup_path = "/home/factorio/server/backup/"

def file_changed():
	global count
	count = count + 1
	if count == 12:
		count = 1
	file_name = backup_path + "_autosave" + str(count) + ".zip"
	copyfile(path, file_name)

while True:
	try:
		if os.path.isfile(path):
			cmtime = os.stat(path).st_mtime
			if cmtime != mtime:
				mtime = cmtime
				file_changed()
		time.sleep(1)
	except KeyboardInterrupt:
		exit(0)
