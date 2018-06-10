while true
do

if [ ! -z $(grep "restart" "./restart") ]; then 

echo "" > ./restart
tmux send-keys -t live '' Enter
tmux send-keys -t live './start.py' Enter
fi
sleep 1
echo "|"
sleep 1
clear
done
