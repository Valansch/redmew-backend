#!/bin/bash

tmux new -s live -d

sleep 0.1
tmux send-keys -t live './start.py' Enter

tmux split-window -v -t live
sleep 0.1
tmux send-keys -t live 'less +F ./log/live.log' Enter

tmux select-pane -U -t live
tmux split-window -h -t live
sleep 0.1
tmux send-keys -t live 'less +F ./log/log.log' Enter
tmux select-pane -L -t live
tmux a -t live
