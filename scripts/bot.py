#!/usr/bin/env python
# vim: set noexpandtab ts=8 sw=8 sts=8 number:

import socket
import re
import os
import discord
import asyncio
import pyotp
import pyinotify
import aiohttp
import random
import luafunctions
from subprocess import Popen
from time import gmtime, strftime, sleep


# Open chatlog file
chatlog_file = 'log/log.log'
port_file_path = 'control_port'
port_file = open(port_file_path, 'r')
chatlog = open(chatlog_file, 'r')
chatlog.seek(0, 2) # Go to the end of the file
api_response_timeout = 3 # seconds
channel = None
# Init socket connection to factorio console
PORT = 0
cwd = os.path.dirname(os.path.abspath(__file__)) + "/../"

with open(cwd + "control_port", 'r') as f:
	PORT = int(f.readlines()[0])
	print("Port: " + str(PORT))
sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest=("localhost", PORT)


class Command:
	is_runable = False
	def __init__(self, name, help_text, implemented=True, output = False, is_function = True, num_args = 0, admin = False):
		self.name = name
		self.help_text = help_text
		self.implemented = implemented
		self.output = output
		self.is_function = is_function
		self.num_args = num_args
		self.admin = admin

	async def run(self, msgid, admin):
		if self.name == "help":
			return commands.print_help()

		if not admin and self.admin: raise RuntimeError("You don't have permission to run this command")	
		if self.is_function:
			first_fct_arg = '"api/' + str(msgid) + '",' if self.output else ","
			template = "/silent-command " + getattr(luafunctions, self.name) + " " + self.name + '(' + first_fct_arg	
			for i in range(1,self.num_args):
				template = template + '"' + call[i] + '",'
			template = template[:-1]
			template = template + ")"
		else:
			template = "/" + " ".join(self.args)
		sckt.sendto(template.encode(), dest)
		if not self.output: return ""			
		filename = cwd + "script-output/api/" + str(msgid)
		tries = 0
		while not os.path.isfile(filename):
			if tries > api_response_timeout * 10:
				return None
			await asyncio.sleep(0.1)
			tries +=1
		response = ""
		with open(filename, "r") as f:
			response = "".join(f.readlines())
		print(response)
		return response
	
	def make_runable(self, args):
		runable = Command(self.name, self.help_text, self.implemented, self.output, self.is_function, self.num_args, self.admin)
		runable.args = args
		runable.is_runable = True
		return runable
class Commands:
	commands = []
	def add(self, command):
		self.commands.append(command)

	def get_command(self, name):
		for c in self.commands: 
			if c.name == name: return c 
		return None
	
	def parse(self, command_str):
		if command_str == "": raise SyntaxError("Empty command.")
		args = command_str.split()
		cmd = self.get_command(args[0])
		if cmd is None: raise SyntaxError("Command not found.")
		if not cmd.implemented: raise SyntaxError("Command not implemented.")
		if not len(args) - 1 == cmd.num_args: raise SyntaxError("{} arguments expected, got {}".format(cmd.num_args,len(args) - 1))
		return cmd.make_runable(args)
		
	
	def print_help(self):
		out = ""
		for c in self.commands:
			out = out + "/" + c.name + " " + c.help_text + "\n"
		return out

 
commands = Commands()
commands.add(Command("help", "Prints this help text"))
commands.add(Command("spy", "spys on a player", implemented=False, num_args=1, is_function = False))
commands.add(Command("players", "lists all online players.", output=True))
commands.add(Command("ban", "bans a player.", is_function=False, num_args=1 , admin=True))
commands.add(Command("unban","unbans a player.", is_function=False, num_args=1, admin=True))
commands.add(Command("time", "How long the server has been running.",is_function=True, output=True))
commands.add(Command("poll", "shows current poll status.",is_function=True, output=True))

def print_to_file(str):
	with open(cwd + "log/bot.log", "a") as f:
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

# Callback for port
def handle_port_change(notifier):
	print("test")
	port_file.seek(0,0)
	line = "".join(port_file.readlines()).rstrip('\n').replace('\n', ' ')

	global dest
	dest=("localhost", int(line))

	print("port changed to:" + line)

# Init event loop for monitoring chatlog and discord events
wm = pyinotify.WatchManager()
loop = asyncio.get_event_loop()
client = discord.Client(loop=loop)
pyinotify.AsyncioNotifier(wm, loop, callback=handle_factorio_chat, default_proc_fun=lambda x: None)
wm.add_watch(chatlog_file, pyinotify.IN_MODIFY)

#maybe i need another loop?
# 2nd watch manager for port file, can i use the same loop? i really only want to watch to file
# with 2 different event handlers
wm2 = pyinotify.WatchManager()
pyinotify.AsyncioNotifier(wm2, loop, callback=handle_port_change, default_proc_fun=lambda x: None)
wm2.add_watch(port_file_path, pyinotify.IN_MODIFY)

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
	global channel
	if not channel:
		channel = discord.Object(id='356780115159547914') # ingame-chat
	if event == "JOIN":
		embed = discord.Embed(title=msg.upper(), color=discord.Color(random.randint(0, 0xFFFFFF)))

		embed.set_image(url=("https://picsum.photos/400/300/?image=" + str(random.randint(0,1084))))
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
		if message.clean_content.startswith("/"):
			print(message.author.name + ": " + message.clean_content)
			try:
				command = commands.parse(message.clean_content[1:])
			except SyntaxError as e:
				await client.send_message(message.channel, e)
				return
			admin = False
			for role in message.author.roles:
				if role.name == "admins": admin = True
			try:
				result = await command.run(message.id, admin)
			except RuntimeError as e:
				await client.send_message(message.channel, e)
				return
			if result is None:
				await client.send_message(message.channel, "Server did not respond.")
			elif not result == "":
				await client.send_message(message.channel, result)

			return
		send_msg_to_game(message.author.name, message.clean_content)

# Run the event loop
client.run('MzU2NTQ2MDI5MDY5NDAyMTE0.DOCnIQ.b25HdFO_9Uz34ose41aen4Oa4AM')
