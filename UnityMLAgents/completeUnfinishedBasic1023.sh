#!/bin/bash


for dir in /home/steinboe/MasterThesis/resultsLinux/*/
do      
        file=$dir"gen1023.json"
        echo $file
        x=1     
        max=10
        while [ ! -f "$file" ]; 
        do      
                echo $dir
                echo "$file does not exist. Checked $x time(s)"
        echo "Running checkpointHPC"
                python3 EvolvingMLAgents.py 0 0 0 0 0 0 --checkpointHPC "$dir"
                x=$((x+1))
                if [ $x -gt $max ]; then
                        echo "breaking"
                        break
                fi
        done
done