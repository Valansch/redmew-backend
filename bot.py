#!/usr/bin/env python
import socket
import re
import os
import discord
import asyncio
from subprocess import Popen

Popen("./upload_chat.sh", shell=True, bufsize=1, universal_newlines=True)
PORT = 0
cwd = os.path.dirname(os.path.abspath(__file__))
with open(cwd + "/control_port", 'r') as f:
	PORT = int(f.readlines()[0])
	print("Port: " + str(PORT))

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest=("localhost", PORT)
client = discord.Client()

def send_msg(username, msg):
	msg = re.sub(r'[\n\r\\"\']', '', msg).strip()
	username = re.sub(r'[\n\r\\"\']', '', username).strip()
	if msg != '':
		template = '/silent-command game.print("[%s@discord]: %s")' % (username, msg)
		print("%s: %s" % (username, msg))
		sckt.sendto(template.encode(), dest)

def spy(username):
	username = re.sub(r'[\n\r\\"\']', '', username).strip()
	template = '/silent-command if spyshot ~= nil then spyshot("%s") end' % username
	sckt.sendto(template.encode(), dest)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.channel.name == 'ingame-chat' and not message.author.bot:
		if message.content.startswith("/spy"):
			matches = re.match("^/spy (.*)", message.content)
			if matches and matches.group(1):
				spy(matches.group(1))
				return
		send_msg(message.author.name, message.content)

client.run('MzU2NTQ2MDI5MDY5NDAyMTE0.DOCnIQ.b25HdFO_9Uz34ose41aen4Oa4AM')
