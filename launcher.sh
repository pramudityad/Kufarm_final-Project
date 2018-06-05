#!/bin/bash

printf '%s\tStart Application\n' "$(date +'%T %A %d %B %Y')" 
sleep 5
cd /
cd /home/pi/Damar/forecast/new
sudo python3 main_lite.py
cd /
