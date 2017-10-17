#!/usr/bin/python

import time
import subprocess

mods 	 = "/home/factorio/server/script-output/mods.lua"
regulars = "/home/factorio/server/script-output/regulars.lua"

time.sleep(30)

def run(cmd):
	subprocess.Popen(cmd)


mods_list = ""
regulars_list = ""
with open(mods, 'r') as myfile:
    mods_list=myfile.read().replace('\n', ' ')
with open(regulars, 'r') as myfile:
    regulars_list=myfile.read().replace('\n', ' ')

command = "tmux send-keys -t console".split()
command.append("/silent-command global.mods = ")
command.append(mods_list)
command.append("Enter")
run(command)
command[len(command) - 3] = "/silent-command global.regulars = "
command[len(command) - 2] = regulars_list
run(command)
