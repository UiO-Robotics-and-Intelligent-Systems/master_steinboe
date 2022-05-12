#!/bin/bash

#Hey! This files checks if a training has stopped, and if so it continues the training! Pure magic

sleep 16 #
#sleep 1 # remove

#for dir in /home/steinboe/M-drive/MasterThesis/resultsArchive/0.1_0.2_0.1_0.01/co-0/*/
for dir in /home/steinboe/MasterThesis/resultsLinux/*/
do
	file=$dir"gen2047.json"
	x=1
	max=10
	while [ ! -f "$file" ]; 
	do
   		echo "$file does not exist. Checked $x time(s)"
		
		# Finding the last file in this dir
		gen=1998
		lastFile=$dir"gen"$gen".json"
		while [ ! -f "$lastFile" ];
		do
		#echo "Could not find $lastFile"
		gen=$((gen-1))
		lastFile=$dir"gen"$gen".json"
		done
		echo "Found $lastFile!"

		if test `find $lastFile -mmin +1`	
		then

		echo "old enough"
		echo "Running checkpointHPC"
		python3 EvolvingMLAgents.py 0 0 0 0 0 0 --checkpointHPC "$dir"
		#python test2.py
		x=$((x+1))
		if [ $x -gt $max ]; then
			echo "breaking"
			break
		fi

		else
		echo "not old enough, breaking"
		break		
		fi		

	done 
	echo "$file does exist!"
done