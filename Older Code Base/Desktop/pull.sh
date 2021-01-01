#!/bin/bash
while true
do 
	rsync -a rushali@192.168.0.103:/home/rushali/opt/flt6/flight2/ /home/manohar/incoming/
	sleep 1
done 
