#!/usr/bin/python
from subprocess import Popen, run, PIPE
import time
import signal
import sys
import os
import select

command_pipe = "/tmp/command_pipeline"
cwd = dir_path = os.path.dirname(os.path.abspath(__file__))

def handler_stop_signal(signum, frame):
	cmd = "killall -s " + str(signum) + " factorio"
	run(cmd, shell=True)
	sys.exit(0)
signal.signal(signal.SIGINT, handler_stop_signal)
signal.signal(signal.SIGTERM, handler_stop_signal)


def get_update_users_command():
	global cwd
	regulars	= cwd + "/script-output/regulars.lua"
	mods	= cwd + "/script-output/mods.lua"
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

cmd = cwd + "/bin/x64/factorio --server-settings " + cwd + "/server-settings.json --start-server " + cwd +"/saves/_autosave1.zip --console-log " + cwd + "/log/diffiebananya03.log"

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
	print("Stopping server", end="")
	run("killall factorio", shell=True)
	#wait up to 20 sec before starting again
	for x in range(20):
		time.sleep(1)
		pid = run("ps -A | grep factorio | awk '{print $1}'", shell=True, stdout=PIPE).stdout.decode('utf-8')
		if pid == "":
			break
		print('.', end='', flush=True)
	print("")
	start()
	sys.exit()

def start():
	global cwd
	print("Starting server.")
	with Popen(cmd + " >> " + cwd + "/log/diffiebananya04live.log", shell=True, stdin=PIPE, bufsize=1, universal_newlines=True) as shell:
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
			if x == 300:
				line = get_update_users_command()
				print(line, file=shell.stdin, flush=True)
try:
	start()
except KeyboardInterrupt:
	sys.exit(0)
