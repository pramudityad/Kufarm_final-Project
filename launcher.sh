#!/bin/bash
printf '%s\tStart Application\n' "$(date +'%T %A %d %B %Y')" 
sleep 5
cd /home/pi/Damar/forecast/new
sudo python3 main2.py & python3 control_panel.py && fg
#sudo nohup python3 main2.py 
cd /
