#!/usr/bin/env python3
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

def log(msg):
    msg = time.strftime("%Y-%m-%d %H:%M:%S: ") + str(msg)
    print(msg)
    with open("./log/python.log", 'a') as f:
        f.write(msg + "\n")


log("Starting script")
log("Control pid: " + str(os.getpid()))
port_number = os.getpid() + 32000 #i feel dirty
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind(('localhost', port_number))

with open("./control_pid", 'w') as f:
    f.write(str(os.getpid()))
with open("./control_port", 'w') as f:
    f.write(str(os.getpid() + 32000))

def get_update_users_command():
    regulars = "./script-output/regulars.lua" 
    print("Updating users")
    cmd = "/silent-command global.regulars = "
    if not os.path.isfile(regulars):
        return "/silent-command log('Updating regulars failed. Missing file: " + regulars + "')"
    with open(regulars, 'r') as f:
        cmd = cmd + f.read().replace('\n', ' ')
    return cmd

def is_stopped():
    global pid
    try:
        os.kill(pid, 0) # PermissionError is deliberatly not caught, because if we get that then something is wrong
    except ProcessLookupError: # errno.ESRCH
        return True # No such process
    return False # no error, we can send a signal to the process

def update():
    log("Updating")
    run("./install.sh --latest", shell=True)
    log("Update finished")

def stop(): 
    log("Stopping server")
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
            if len(line) > 1 and line[0] == ":":
                parse_and_execute(line[1:], None)

def restart():
    stop(false)
    for x in range(10000000):
        time.sleep(1)
        if is_stopped(): break
    log("Loading latest save file")
    start()
    sys.exit(0)

def load_save(file):
    file = file.strip()
    if file == "":
        file = "saves/_autosave1.zip"
    file = os.path.join("./", file) 
    if not os.path.isfile(file):
        log("File does not exist.")
        return 0
    stop(false)
    for x in range(10000000):
        time.sleep(1)
        if is_stopped(): break
    log("Loading " + file)
    deflate.clean_save(file, "./saves/current_map.zip")
    global cmd
    cmd = load_save_cmd
    start()
    sys.exit(0)

def load_scenario():
    if not is_stopped(): 
        stop()
        log("stopping server")
    time.sleep(5)
    for x in range(10000000):
        time.sleep(5)
        if is_stopped(): break
        stop()
        log("tryping again")
    log("Loading scenario RedMew")
    global start_scenario_cmd
    global cmd
    cmd = start_scenario_cmd
    start()
    sys.exit(0)

def fileop(command):
    if (command.find("rm") == 0):
        try:
            os.remove(os.path.join("./saves/", command[2:].strip()))
        except Exception as e:
            log(e)
    elif(command.find("mv") == 0):
        params = command.split()
        if len(params) == 3:
            file1 = os.path.join("./saves", params[1])
            file2 = os.path.join("./saves", params[2])
            try:
                os.rename(file1, file2)
                log("mv " + file1 + " " + file2 + ": success.")
            except Exception as e:
                log(e) 
        else:
            log("Wrong number of arguments to: mv")
    else:
        log("Unsupported file operation: " + command)
def parse_and_execute(command, shell):
    log("Received command " + command)
    command = command.rstrip("\n")
    if command == "":
        pass
    elif command[:4] == "stop":
        if is_stopped(): log("Server is already stopped")
        else:
            stop()
            change_state_stopped()
    elif command == "start":
        if is_stopped():
            global load_save_cmd
            global cmd
            cmd = load_save_cmd
            start()
        else: log("Server already running")
    elif command.find("loadscenario") == 0:
        load_scenario()
    elif command.find("loadsave") == 0:
        load_save(command[8:])
    elif command.find("fo") == 0:
        fileop(command[2:].strip())
    elif command == "restart":
        restart()
    elif command == "kill":
        log("Shutting down")
        stop()
        sys.exit(0)
    elif command == "update":
        stop(false)
        update()
        start()
    elif command == "save":
        if shell:
            print("/silent-command game.server_save()", file=shell.stdin, flush=True)
    else:
        log("Unknown command: " + command)
def start():
    global pid
    global cmd
    global mySocket

    log("Starting server with info " + cmd)
    with Popen(cmd + " >> " + live_log, shell=True, stdin=PIPE, bufsize=1, universal_newlines=True) as shell:
        pid = shell.pid + 2
        update_external_pid()
        for x in range(100000000):
            #Check for input every 0.1 sec
            #stdin
            if x > 50 and is_stopped():
                log("Crash detected")
                restart()
                sys.exit(0)
            try:
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    line = sys.stdin.readline()
                    if len(line) > 0:
                        if line[0] == ":":
                            parse_and_execute(line[1:], shell)
                        else:
                            print(line, file=shell.stdin, flush=True)
            except BrokenPipeError:
                log("Broken pipe")
                restart()
                sys.exit(0)
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
    log("Bye.")
