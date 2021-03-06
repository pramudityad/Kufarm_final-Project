#!/bin/bash

#cari semua PID
$pid=`ps ax | grep 'main2.py'`

#jika PID tidak ditemukan maka print empty, jika isi maka di kill
if [ -z $pid ]
then
	echo "empty"
else
	sudo kill -9 $pid
	printf '%s\tStop Application\n' "$(date +'%T %A %d %B %Y')" >>/home/pi/Damar/forecast/logs/restartlog
fi

#start semua program
sleep 5
printf '%s\tStart Application\n' "$(date +'%T %A %d %B %Y')" >>/home/pi/Damar/forecast/logs/restartlog
cd /home/pi/Damar/forecast/new
sudo python3 /home/pi/Damar/forecast/new/main2.py & python3 /home/pi/Damar/forecast/new/control_panel.py && fg
#sudo python3 /home/pi/Damar/forecast/new/main2.py
