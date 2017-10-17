#!/usr/bin/python
cmd = "/home/factorio/server/bin/x64/factorio --server-settings /home/factorio/server/server-settings.json --start-server /home/factorio/server/saves/_autosave1.zip --console-log /home/factorio/server/log/diffiebananya03.log"

update_users="/home/factorio/server/update_users.py"

$update_users &

 /home/factorio/server/parameter_start.sh >> 
/home/factorio/server/log/diffiebananya04live.log

