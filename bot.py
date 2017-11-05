#!/usr/bin/env python
import socket
import re
import os
import discord
import asyncio

PORT = 0
cwd = os.path.dirname(os.path.abspath(__file__))
with open(cwd + "/control_port", 'r') as f:
	PORT = int(f.readlines()[0])
	print("Port: " + str(PORT))

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest=("localhost", PORT)
client = discord.Client()

def send_msg(username, msg):
	msg = re.sub(r'[^A-Za-z0-9 ]', '', msg).strip()
	username = re.sub(r'[^A-Za-z0-9 ]', '', username).strip()
	if msg != '':
		template = '/silent-command game.print("[%s@discord]: %s")' % (username, msg)
		print("%s: %s" % (username, msg))
		sckt.sendto(template.encode(), dest)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.channel.name == 'ingame-chat' and !message.author.bot:
		send_msg(message.author.name, message.content)

client.run('MzU2NTQ2MDI5MDY5NDAyMTE0.DOCnIQ.b25HdFO_9Uz34ose41aen4Oa4AM')
