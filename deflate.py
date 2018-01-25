#!/usr/bin/python
import glob
import os.path
import zipfile
import shutil
import math

dir_name = ""
inlcuded_files = []
logfile = "./log/live.log"

def log(str):
	with open(logfile, 'a') as f:
		f.write("[Save deflation] " + str + "\n")

def parse_URI(line):
    line = line.replace("(", " ").replace(")","").replace("\"","").replace(".","/").replace(" ", "")
    line = line[(line.find("require") + 7):] + ".lua"
    URI = dir_name + line
    if os.path.exists(URI) and URI not in inlcuded_files:
        inlcuded_files.append(URI)
        parse_file(line)

def parse_line(line):
    if "require" in line:
        if not "--" in line or line.find("--") > line.find("require"):
            parse_URI(line)

def parse_file(file_name):
    f = open(dir_name + file_name, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        parse_line(line.rstrip())

def unzip(save_name):
    global dir_name
    dir_name = save_name[:save_name.find(".zip")] + "/"
    if os.path.isdir(dir_name):
        log("Deleting directory " + dir_name)
        shutil.rmtree(dir_name)
    zip_ref = zipfile.ZipFile(save_name, 'r')
    zip_ref.extractall(os.path.dirname(save_name))
    zip_ref.close()

def zip(dir_name, save_name):
    to_zip = os.path.join(os.path.dirname(save_name), "to_zip")
    if not os.path.exists(to_zip):
        os.makedirs(to_zip)
    shutil.move(dir_name, to_zip)

    shutil.make_archive(save_name[:-4], 'zip', to_zip)

    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)

    if os.path.isdir(to_zip):
        shutil.rmtree(to_zip)

def remove_unwanted_files():
    for filename in glob.iglob(dir_name + '**/*', recursive=True):
        if filename not in inlcuded_files and os.path.isfile(filename) and filename.find("locale/") == -1:
            log("Removing " + filename)
            with open(filename, "w") as f:
                f.write("This file was removed to reduce save size. If you downloaded this scenario and are interested in downloading the  full version, visit github.com/valansch/redmew\n")

def add_excemptions():
    global inlcuded_files
    inlcuded_files.append(dir_name + "control.lua")
    inlcuded_files.append(dir_name + "level-init.dat")
    inlcuded_files.append(dir_name + "level.dat")
    inlcuded_files.append(dir_name + "script.dat")
    inlcuded_files.append(dir_name + "info.json")

def clean_save(save_name, output_name):
    file_size_before = os.path.getsize(save_name)
    unzip(save_name)
    add_excemptions()
    parse_file("control.lua")
    remove_unwanted_files()
    zip(dir_name, save_name)
    file_size_after = os.path.getsize(save_name)
    log("File size reduced by " + str(100 - math.floor(1000 * file_size_after / file_size_before)/10) + "%")

