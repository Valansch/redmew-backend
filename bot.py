#!/usr/bin/env python
import socket
import re
import os
import discord
import asyncio
import pyotp
import pyinotify
import aiohttp
import random
from subprocess import Popen
from time import gmtime, strftime

# Open chatlog file
chatlog_file = 'log/log.log'
chatlog = open(chatlog_file, 'r')
chatlog.seek(0, 2) # Go to the end of the file

# Init socket connection to factorio console
PORT = 0
cwd = os.path.dirname(os.path.abspath(__file__))
with open(cwd + "/control_port", 'r') as f:
	PORT = int(f.readlines()[0])
	print("Port: " + str(PORT))
sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest=("localhost", PORT)

# Read admin auth token for discord command execution
# Init TOTP and remember most recent password
ADMIN_TOKEN = ''
with open(cwd + "/admin_secret", "r") as f:
	ADMIN_TOKEN = f.readlines()[0].rstrip('\n')
totp = pyotp.TOTP(ADMIN_TOKEN)
lastpass = totp.now()

# Store the candidate :D
pending_ban = None

def print_to_file(str):
	with open(cwd + "/log/bot.log", "a") as f:
		f.write(str + "\n")

# Callback for chatlog monitor
def handle_factorio_chat(notifier):
	line = "".join(chatlog.readlines()).rstrip('\n').replace('\n', ' ')
	matches = re.match(r"[0-9-]* [0-9:]* \[([A-Z]*)\] (.*)", line)
	if matches and matches.group(1) and matches.group(2):
		event = matches.group(1)
		msg = matches.group(2)
		print_to_file(line)
		notifier.loop.create_task(send_msg_to_discord(event, msg))

# Init event loop for monitoring chatlog and discord events
wm = pyinotify.WatchManager()
loop = asyncio.get_event_loop()
client = discord.Client(loop=loop)
notifier = pyinotify.AsyncioNotifier(wm, loop, callback=handle_factorio_chat, default_proc_fun=lambda x: None)
wm.add_watch(chatlog_file, pyinotify.IN_MODIFY)

def replace_mentions(match):
	username = match.group(1)
	server = client.get_server('312150126766456832') # redmew server
	member = server.get_member_named(username)
	if member != None:
		return member.mention
	else:
		return match.group(0)

async def send_msg_to_discord(event, msg):
	print(msg)
	msg = re.sub(r"@(\S+)", replace_mentions, msg)
	server = client.get_server('312150126766456832') # redmew server
	channel = discord.Object(id='356780115159547914') # ingame-chat
	if event == "JOIN":
		embed = discord.Embed(title=msg.upper(), color=discord.Color(random.randint(0, 0xFFFFFF)))
		async with aiohttp.request('GET', 'http://random.cat/meow') as resp:
			if resp.status == 200:
				cat_img = await resp.json()
				embed.set_image(url=cat_img["file"])
		sent_msg = await client.send_message(channel, embed=embed)
		emojis = random.sample(server.emojis, 3)
		for emo in emojis:
			await client.add_reaction(sent_msg, emo)
	else:
		await client.send_message(channel, msg)

def send_msg_to_game(username, msg):
	msg = re.sub(r'[\n\r\\"\']', '', msg).strip()
	username = re.sub(r'[\n\r\\"\']', '', username).strip()
	if msg != '':
		template = '/silent-command game.print("[%s@discord]: %s")' % (username, msg)
		print("%s: %s" % (username, msg))
		print_to_file("%s %s@discord: %s" % (strftime("%Y-%m-%d %X [CHAT]", gmtime()), username, msg))
		sckt.sendto(template.encode(), dest)

def spy(username):
	username = re.sub(r'[\n\r\\"\']', '', username).strip()
	template = '/spyshot %s' % username
	sckt.sendto(template.encode(), dest)

def ban(username):
	username = re.sub(r'[\n\r\\"\']', '', username).strip()
	template = '/ban %s' % username
	sckt.sendto(template.encode(), dest)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	global pending_ban
	global lastpass
	if message.channel.name == 'ingame-chat' and not message.author.bot:
		if message.content.startswith("/spy"):
			matches = re.match("^/spy (.*)", message.content)
			if matches and matches.group(1):
				spy(matches.group(1))
				return
		if message.content.startswith("/ban"):
			matches = re.match("^/ban (.*)", message.content)
			if matches and matches.group(1):
				pending_ban = matches.group(1)
				await client.send_message(message.channel, 'Enter your password to ban user {}.'.format(pending_ban))
				return
		if re.match("^[0-9]{6}$", message.content):
			if pending_ban != None:
				if message.content == totp.now() and message.content != lastpass:
					ban(pending_ban)
					pending_ban = None
					lastpass = message.content
				else:
					await client.send_message(message.channel, 'Wrong password.')
				return
		send_msg_to_game(message.author.name, message.clean_content)

# Run the event loop
client.run('MzU2NTQ2MDI5MDY5NDAyMTE0.DOCnIQ.b25HdFO_9Uz34ose41aen4Oa4AM')
