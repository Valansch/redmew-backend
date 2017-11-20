#!/usr/bin/python
from subprocess import Popen, run, PIPE, check_output
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time
import signal
import sys
import os
import select

cwd = os.path.dirname(os.path.abspath(__file__))
pid = 0
live_log = cwd + "/log/live.log"
log = cwd + "/log/log.log"
bind_arg = " --bind 5.9.164.209"
if (len(sys.argv) > 1 and sys.argv[1] == "-nobind"):
	bind_arg = ""

cmd = cwd + "/bin/x64/factorio --server-settings " + cwd + "/server-settings.json --start-server-load-latest --console-log " + log + bind_arg

print("Controlpid: " + str(os.getpid()))
port_number = os.getpid() + 32000 #i feel dirty
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind(('localhost', port_number))


with open(cwd + "/control_pid", 'w') as f:
	f.write(str(os.getpid()))
with open(cwd + "/control_port", 'w') as f:
	f.write(str(os.getpid() + 32000))

def get_update_users_command():
	global cwd
	regulars	= cwd + "/script-output/regulars.lua"
	mods	= cwd + "/script-output/mods.lua"
	print("Updating users")
	cmd = " global.regulars = "
	if not os.path.isfile(regulars):
		return "/silent-command log('Updating regulars failed. Missing file: " + regulars + "')"
	if not os.path.isfile(mods):
		return "/silent-command log('Updating regulars failed. Missing file: " + mods + "')"
	with open(regulars, 'r') as f:
		cmd = cmd + f.read().replace('\n', ' ')
	with open(mods, 'r') as f:
		cmd = f.read().replace('\n', ' ') + cmd
	return "/silent-command global.mods = " + cmd

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

def update_external_pid():
	global pid
	with open(cwd + "/factorio_pid", 'w') as f:
		f.write(str(pid))

def change_state_stopped():
	global mySocket
	for x in range(1000000):
		#Check for input every 0.1 sec
		#stdin
		if select.select([sys.stdin], [], [], 0.1)[0]:
			line = sys.stdin.readline()
			if len(line) > 0:
				if line[0] == ":":
					parse_and_execute(line[1:], None)
		#external cmd
		if select.select([mySocket], [], [], 0.1)[0]:
			(data, _) = mySocket.recvfrom(16384)
			line = data.decode('UTF-8')
			if line[0] == ":":
				parse_and_execute(line[1:], None)

def restart():
	stop()
	for x in range(10000000):
		time.sleep(1)
		if is_stopped(): break
	print("Loading latest save file")
	start()
	sys.exit(0)

def parse_and_execute(command, shell):
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
	elif command == "save":
		if shell:
			print("/silent-command game.server_save()", file=shell.stdin, flush=True)
	else:
		print("Unknown command: " + command)
def start():
	global cwd
	global pid
	global cmd
	global mySocket

	print("Starting server with info " + cmd)
	with Popen(cmd + " >> " + live_log, shell=True, stdin=PIPE, bufsize=1, universal_newlines=True) as shell:
		pid = shell.pid + 2
		update_external_pid()
		for x in range(100000000):
			#Check for input every 0.1 sec
			#stdin
			if select.select([sys.stdin], [], [], 0.1)[0]:
				line = sys.stdin.readline()
				if len(line) > 0:
					if line[0] == ":":
						parse_and_execute(line[1:], shell)
					else:
						print(line, file=shell.stdin, flush=True)
			#external cmd
			if select.select([mySocket], [], [], 0.1)[0]:
				(data, _) = mySocket.recvfrom(16384)
				line = data.decode('UTF-8')
				if line[0] == ":":
					parse_and_execute(line[1:], shell)
				else:
					print(line, file=shell.stdin, flush=True)
			#Update users after 20 sec
			if x == 100:
				line = get_update_users_command()
				print(line, file=shell.stdin, flush=True)

try:
	start()
except KeyboardInterrupt:
	print("Bye.")
