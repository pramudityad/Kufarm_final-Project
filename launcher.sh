#!/bin/bash

printf '%s\tStart Application\n' "$(date +'%T %A %d %B %Y')" 
sleep 3
cd /
cd /home/pi/Damar/forecast/new
sudo python3 main.py
cd /
