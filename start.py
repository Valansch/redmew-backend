#!/usr/bin/python3
from subprocess import Popen, run, PIPE
import time
import signal
import sys
import os
import select

cwd = os.path.dirname(os.path.abspath(__file__))
command_pipe = "/tmp/command_pipeline" + cwd + "/pipe"
pid = 0
live_log = cwd + "/log/live.log"
log = cwd + "/log/log.log"
cmd = cwd + "/bin/x64/factorio --server-settings " + cwd + "/server-settings.json --start-server " + cwd + "/saves/_autosave1.zip --console-log " + log #+ " --bind 5.9.164.209"

with open(cwd + "/control_pid", 'w') as f:
	f.write(str(os.getpid()))

def handler_stop_signal(signum, frame):
	global pid
	if not is_stopped():
		cmd = "kill -s " + str(signum) + " " + str(pid)
		run(cmd, shell=True)
	sys.exit(0)
signal.signal(signal.SIGINT, handler_stop_signal)
signal.signal(signal.SIGTERM, handler_stop_signal)


def get_update_users_command():
	global cwd
	regulars	= cwd + "/script-output/regulars.lua"
	mods	= cwd + "/script-output/mods.lua"
	print("Updating users")
	cmd = " global.regulars = "
	with open(regulars, 'r') as f:
		cmd = cmd + f.read().replace('\n', ' ')
	with open(mods, 'r') as f:
		cmd = f.read().replace('\n', ' ') + cmd
	return "/silent-command global.mods = " + cmd

def get_external_command():
	if os.path.isfile(command_pipe):
		line = ""
		with open(command_pipe) as f:
			line = f.readline().rstrip(" ").rstrip("\n")
		os.remove(command_pipe)
		print("Received external command " + line)
		return line
	else:
		return ""

def is_stopped():
	global pid
	try:
		os.kill(pid, 0) # PermissionError is deliberatly not caught, because if we get that then something is wrong
	except ProcessLookupError: # errno.ESRCH
		return True # No such process
	return False # no error, we can send a signal to the process

def update():
	global cwd
	print("Updating")
	run(cwd + "/update.sh", shell=True)

def stop():
	if not is_stopped():
		print("Stopping server")
		run("kill " + str(pid), shell=True)

def update_external_status():
	global pid
	with open(cwd + "/pid", 'w') as f:
		f.write(pid)

def change_state_stopped():
	for x in range(1000000):
		#Check for input every 0.1 sec
		if select.select([sys.stdin], [], [], 0.1)[0]:
			line = sys.stdin.readline()
			if len(line) > 0 and line[0] == ":":
				parse_and_execute(line[1:])
		if x % 20 == 0:
			command = get_external_command()
			parse_and_execute(command)

def restart():
	stop()
	#wait up to 20 sec before starting again
	for x in range(10000000):
		time.sleep(1)
		if is_stopped(): break
	start()
	sys.exit(0)

def parse_and_execute(command):
	command = command.rstrip("\n")
	if command == "":
		pass
	elif command == "stop":
		if is_stopped(): print("Server is already stopped")
		else:
			stop()
			change_state_stopped()
	elif command == "start":
		if is_stopped():
			start()
		else: print("Server already running")
	elif command == "restart":
		restart()
	elif command == "update":
		stop()
		update()
		start()
	else:
		print("Unknown command: " + command)
def start():
	global cwd
	global pid
	print("Starting server")
	with Popen(cmd + " >> " + live_log, shell=True, stdin=PIPE, bufsize=1, universal_newlines=True) as shell:
		pid = shell.pid + 1
		update_external_pid()
		for x in range(100000000):
			#Check for input every 0.1 sec
			if select.select([sys.stdin], [], [], 0.1)[0]:
				line = sys.stdin.readline()
				if len(line) > 0:
					if line[0] == ":":
						parse_and_execute(line[1:])
					else:
						print(line, file=shell.stdin, flush=True)
			#Check for command every 2 sec
			if x % 20 == 0:
				command = get_external_command()
				parse_and_execute(command)
			#Update users after 30 sec
			if x == 300:
				line = get_update_users_command()
				print(line, file=shell.stdin, flush=True)
try:
	start()
except KeyboardInterrupt:
	sys.exit(0)
