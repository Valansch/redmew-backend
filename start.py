#!/usr/bin/python
from subprocess import Popen, run, PIPE
import time
import signal
import sys
import os
import select

cwd = os.path.dirname(os.path.abspath(__file__))
command_pipe = "/tmp/command_pipeline" + cwd + "/pipe"
pid = 0
def handler_stop_signal(signum, frame):
	global pid
	cmd = "kill -s " + str(signum) + " " + str(pid)
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

cmd = cwd + "/bin/x64/factorio --server-settings " + cwd + "/server-settings.json --start-server " + cwd + "/saves/_autosave1.zip --console-log " + cwd + "/log/diffiebananya03.log --bind 5.9.164.209"

def pid_exists(pid):
	try:
		os.kill(pid, 0) # PermissionError is deliberatly not caught, because if we get that then something is wrong
	except ProcessLookupError: # errno.ESRCH
		return False # No such process
	return True # no error, we can send a signal to the process
def update():
	global cwd
	print("Updating.")
	run(cwd + "/update.sh", shell=True)

def stop():
	global pid
	if pid_exists(pid):
		print("Stopping server.")
		run("kill " + str(pid), shell=True)

def stopped():
	for x in range(1000000):
		time.sleep(2)
		command = get_command()
		if command == "start":
			start()
			sys.exit(0)
		elif command == "update":
			update()

def restart():
	global pid
	stop()
	#wait up to 20 sec before starting again
	for x in range(10000000):
		time.sleep(1)
		if not pid_exists(pid): break
		if x > 0: print('.', end='', flush=True)
	print("")
	start()
	sys.exit(0)

def start():
	global cwd
	global pid
	print("Starting server.")
	with Popen(cmd + " >> " + cwd + "/log/diffiebananya04live.log", shell=True, stdin=PIPE, bufsize=1, universal_newlines=True) as shell:
		pid = shell.pid + 1
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
				elif command == "update":
					stop()
					update()
					start()
			#Update users after 30 sec
			if x == 300:
				line = get_update_users_command()
				print(line, file=shell.stdin, flush=True)
try:
	start()
except KeyboardInterrupt:
	sys.exit(0)

