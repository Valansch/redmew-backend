#!/usr/bin/python
from subprocess import Popen, run, PIPE, STDOUT
import time
import signal
import sys
import os

print(os.getpid())
def handler_stop_signal(signum, frame):
	print("Test")
	raise KeyboardInterrupt
signal.signal(signal.SIGINT, handler_stop_signal)
signal.signal(signal.SIGTERM, handler_stop_signal)

def update_users():
	mods     = "/home/factorio/server/script-output/mods.lua"
	regulars = "/home/factorio/server/script-output/regulars.lua"

	time.sleep(30)

	print("Updating users...")

	mods_list = ""
	regulars_list = ""
	with open(mods, 'r') as myfile:
	    mods_list=myfile.read().replace('\n', ' ')
	with open(regulars, 'r') as myfile:
	    regulars_list=myfile.read().replace('\n', ' ')

	command = "tmux send-keys -t console".split()
	command.append("/silent-command global.mods = ")
	command.append(mods_list)
	command.append("Enter")
	Popen(command)
	command[len(command) - 3] = "/silent-command global.regulars = "
	command[len(command) - 2] = regulars_list
	Popen(command)


cmd = "/home/factorio/server/bin/x64/factorio --server-settings /home/factorio/server/server-settings.json --start-server /home/factorio/server/saves/_autosave1.zip --console-log /home/factorio/server/log/diffiebananya03.log"

#update_users()

print("Starting server.")
try:
	run(cmd + " >> /home/factorio/server/log/diffiebananya04live.log", shell=True, stdin=sys.stdin)
except KeyboardInterrupt:
	print("Server stopped by Keyboard Interrupt")

