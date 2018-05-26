#!/bin/bash

printf '%s\tStart Application\n' "$(date +'%T %A %d %B %Y')" 
sleep 5
cd /
cd home/pi/Desktop/Damar/forecast/new/
sudo python input_data.py
cd /
