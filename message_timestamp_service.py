#!/usr/bin/python
import time
import os.path
filename = "/opt/factorio/script-output/chatlog.txt"

while True:
	if os.path.isfile(filename):
		with open(filename) as file:
			lines = file.readlines()
		for line in lines:
			print(line)
		os.remove(filename)

	time.sleep(1)
