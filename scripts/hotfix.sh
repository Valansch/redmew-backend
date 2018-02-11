#!/bin/sh

root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../"
PID=$(<$root_dir"factorio_pid")
cd $root_dir"saves/"
tmux send-keys -t $1 "/silent-command game.server_save('_autosave1.zip')"
tmux send-keys -t $1 Enter
sleep 4
kill -KILL $PID
unzip _autosave1.zip
Yes | cp -rf hotfix/* _autosave1/
mv _autosave1.zip _autosave1.zip_backup
zip -r _autosave1.zip _autosave1/
rm -rf _autosave1/

tmux send-keys -t $1 :start Enter
