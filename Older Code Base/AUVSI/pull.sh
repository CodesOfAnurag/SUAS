#!/bin/bash
while true
do 
	rsync -a odroid@192.168.1.6:/home/odroid/Desktop/interop-master/client/WiringPi2-Python/examples/flight4/ /home/manohar/incoming/
	sleep 1
done 
