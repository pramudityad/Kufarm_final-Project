#!/bin/bash

#cari semua PID
pid=`ps aux | grep 'main2.py' | awk '{print $2}'`

#jika PID tidak ditemukan maka print empty, jika isi maka di kill
if [ -z $pid ]
then
	echo "empty"
else
	sudo kill -9 $pid
	printf '%s\tStop Application\n' "$(date +'%T %A %d %B %Y')" >>/home/pi/Damar/forecast/logs/restartlog
fi

#start semua program
printf '%s\tStart Application\n' "$(date +'%T %A %d %B %Y')" >>/home/pi/Damar/forecast/logs/restartlog
cd /home/pi/Damar/forecast/new
rm -f /home/pi/Damar/forecast/new/nohub.out
nohup python3 /home/pi/Damar/forecast/new/main2.py &
