#!/bin/bash

#cari semua PID
<<<<<<< HEAD
$pid=`ps ax | grep 'main2.py'`
=======
$pid=`ps aux | grep 'main2.py'`
>>>>>>> 7057002ba4b5548ad8d193ab91814ee3f78e1e49

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
rm -f /home/pi/Damar/forecast/new/nohub.out
<<<<<<< HEAD
nohup python3 /home/pi/Damar/forecast/new/main2.py & python3 /home/pi/Damar/forecast/new/control_panel.py && fg
=======
nohup python3 /home/pi/Damar/forecast/new/main2.py & python3 /home/pi/Damar/forecast/new/control_panel.py && fg
>>>>>>> 7057002ba4b5548ad8d193ab91814ee3f78e1e49
