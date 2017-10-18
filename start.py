#!/usr/bin/python
from subprocess import Popen, run, PIPE, STDOUT
import time
import signal
import sys
import os
import select

command_pipe = "/tmp/command_pipeline"
status = "stopped"

def handler_stop_signal(signum, frame):
	cmd = "killall -s " + str(signum) + " factorio"
	run(cmd, shell=True)
#signal.signal(signal.SIGINT, handler_stop_signal)
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
	if os.path.isfile(command_pipe):
		line = ""
		with open(command_pipe) as f:
			line = f.readline().rstrip(" ").rstrip("\n")
		os.remove(command_pipe)
		return line
	else:
		return ""

cmd = "/home/factorio/server/bin/x64/factorio --server-settings /home/factorio/server/server-settings.json --start-server /home/factorio/server/saves/_autosave1.zip --console-log /home/factorio/server/log/diffiebananya03.log"

def stop():
	print("Stopping server.")
	run("killall factorio", shell=True)

def stopped():
	for x in range(1000000):
		time.sleep(2)
		command = get_command()
		if command == "start":
			start()
			sys.exit()

def restart():
	stop()
	time.sleep(5)
	start()
	sys.exit()

def start():
	print("Starting server.")
	with Popen(cmd + " >> /home/factorio/server/log/diffiebananya04live.log", shell=True, stdin=PIPE, bufsize=1, universal_newlines=True) as shell:
		for x in range(1000):
			if select.select([sys.stdin], [], [], 0.1)[0]:
				line = sys.stdin.readline()
				print(line, file=shell.stdin, flush=True)
			if x % 20 == 0:
				command = get_command()
				if command == "stop":
					stop()
					stopped()
				elif command == "restart":
					restart()
try:
	start()
except KeyboardInterrupt:
	sys.exit(0)
