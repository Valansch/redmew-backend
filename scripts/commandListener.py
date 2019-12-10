#!/usr/bin/env python3
# vim: set noexpandtab ts=8 sw=8 sts=8 number:

import socket
import re
import sys
import os
import pyotp

from time import gmtime, strftime, sleep

# Open chatlog file

chatlog_file = '/home/factorio/server/log/log.log'
port_file_path = '/home/factorio/server/control_port'
command_file_path = '/home/factorio/server/script-output/commandPipe'

# Init socket connection to factorio console
port= 0
cwd = os.path.dirname(os.path.abspath(__file__)) + "/../"

with open(cwd + "control_port", 'r') as f:
	port = int(f.readlines()[0])
	print("Port: " + str(port))
sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest=("localhost", port)

open(command_file_path, 'w').close();

 
def print_to_file(str):
	with open(cwd + "log/bot.log", "a") as f:
		f.write(str + "\n")

# Callback for port
def check_port():
	line = ""
	with open(port_file_path, 'r') as f:
		f.seek(0,0)
		line = "".join(f.readlines()).rstrip('\n').replace('\n', ' ')
	global port
	if port != int(line):
		global dest
		dest=("localhost", int(line))
		port = int(line)
		print("port changed to:" + line)

#Callback for command
def check_command():
	line = ""
	with open(command_file_path, 'r') as f:
		f.seek(0,0)
		line = "".join(f.readlines()).rstrip('\n').replace('\n', ' ')

	if line:
		print(line)
		send_msg_to_game(line)
		open(command_file_path, 'w').close();
	

def send_msg_to_game(msg):
	if msg != '':			
		sckt.sendto(msg.encode(), dest)

while (True):
	sleep(1)
	check_port();
	check_command()
