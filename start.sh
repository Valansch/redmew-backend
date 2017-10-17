cmd="/home/factorio/server/backup.py"

$cmd &

pid=$!

#trap "kill 15 $pid" INT

update_users="/home/factorio/server/update_users.py"

$update_users &

until /home/factorio/server/parameter_start.sh;
do echo "Server died with $2. Restarting..." >&2;
sleep 1;
done >> /home/factorio/server/log/diffiebananya04live.log
