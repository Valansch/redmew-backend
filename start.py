#!/usr/bin/python
from subprocess import Popen, run, PIPE, STDOUT
import time
import signal
import sys
import os

f = open("/home/factorio/server/pid",'w')
f.write(str(os.getpid()))
f.close()
command_pipe = "/home/factorio/server/command"

def handler_stop_signal(signum, frame):
	cmd = "killall -s " + str(signum) + " factorio"
	run(cmd, shell=True)
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

def get_command():


cmd = "/home/factorio/server/bin/x64/factorio --server-settings /home/factorio/server/server-settings.json --start-server /home/factorio/server/saves/_autosave1.zip --console-log /home/factorio/server/log/diffiebananya03.log"

#update_users()

def start_server():
	try:
		print("Starting server.")
		p = Popen(cmd + " >> /home/factorio/server/log/diffiebananya04live.log", shell=True, stdin=PIPE)
	except KeyboardInterrupt:
		print("Server stopped by Keyboard Interrupt")

start_server()

while True:
	time.sleep(1)
	command = ""
	with open(command_pipe) as f:
		command = f.readlines()
	print(command)
