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

def get_update_users_command():
	regulars	= "/home/factorio/server/script-output/regulars.lua"
	mods	= "/home/factorio/server/script-output/mods.lua"
	print("Updating users.")
	cmd = " global.regulars = "
	with open(regulars, 'r') as f:
		cmd = cmd + f.read().replace('\n', ' ')
	with open(mods, 'r') as f:
		cmd = f.read().replace('\n', ' ') + cmd
	return "/silent-command global.mods = " + cmd

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
		for x in range(100000000):
			#Check for input every 0.1 sec
			if select.select([sys.stdin], [], [], 0.1)[0]:
				line = sys.stdin.readline()
				print(line, file=shell.stdin, flush=True)
			#Check for command every 2 sec
			if x % 20 == 0:
				command = get_command()
				if command == "stop":
					stop()
					stopped()
				elif command == "restart":
					restart()
			#Update users after 30 sec
			if x == 50:
				line = get_update_users_command()
				print(line, file=shell.stdin, flush=True)
try:
	start()
except KeyboardInterrupt:
	sys.exit(0)
