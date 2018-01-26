#!/usr/bin/python
from subprocess import Popen, run, PIPE, check_output
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import time
import signal
import sys
import os
import select
import os.path
import deflate

pid = 99999
live_log = "./log/live.log"
log = "./log/log.log"
bind_arg = " --bind 5.9.164.209"
if (len(sys.argv) > 1 and sys.argv[1] == "-nobind"):
	bind_arg = ""

load_save_cmd = "./bin/x64/factorio --server-settings ./server-settings.json --start-server-load-latest --console-log " + log + bind_arg
start_scenario_cmd = "./bin/x64/factorio --server-settings ./server-settings.json --start-server-load-scenario RedMew --console-log " + log + bind_arg
cmd = load_save_cmd

print("Control pid: " + str(os.getpid()))
port_number = os.getpid() + 32000 #i feel dirty
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind(('localhost', port_number))


with open("./control_pid", 'w') as f:
	f.write(str(os.getpid()))
with open("./control_port", 'w') as f:
	f.write(str(os.getpid() + 32000))

def get_update_users_command():
	regulars	= "./script-output/regulars.lua"
	mods	= "./script-output/mods.lua"
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
	print("Updating")
	run("./install.sh --latest", shell=True)

def stop():
	if not is_stopped():
		print("Stopping server")
		run("kill " + str(pid), shell=True)

def update_external_pid():
	global pid
	with open("./factorio_pid", 'w') as f:
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

def load_save(file):
	file = file.replace(" ", "")
	if file == "":
		file = "saves/_autosave1.zip"
	file = os.path.join("./", file)
	if not os.path.isfile(file):
		print("File does not exist.")
		return 0
	stop()
	for x in range(10000000):
		time.sleep(1)
		if is_stopped(): break
	print("Loading " + file)

	deflate.clean_save(file, "./saves/current_map.zip")

	global load_save_cmd
	global cmd
	cmd = load_save_cmd
	start()
	sys.exit(0)

def load_scenario():
	if not is_stopped(): stop()
	for x in range(10000000):
		time.sleep(1)
		if is_stopped(): break
	print("Loading scenario RedMew")
	global start_scenario_cmd
	global cmd
	cmd = start_scenario_cmd
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
			global load_save_cmd
			global cmd
			cmd = load_save_cmd
			start()
		else: print("Server already running")
	elif command == "loadscenario":
		load_scenario()
	elif command.find("loadsave") == 0:
		load_save(command[8:])
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
				try:
					print("/silent-command ", file=shell.stdin, flush=True)
					print(line, file=shell.stdin, flush=True)
				except BrokenPipeError:
					restart()
try:
	print("Enter :start to load the latest save file.")
	print("Enter :loadsave to load saves/_savefile1.zip.")
	print("Enter :loadsave <path> to load a save file.")
	change_state_stopped()
except KeyboardInterrupt:
	print("Bye.")
