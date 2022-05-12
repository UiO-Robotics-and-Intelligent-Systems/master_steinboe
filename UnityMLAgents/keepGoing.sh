#!/bin/bash
maxtime=640
jobList=(
"NAME"
"keepG"
"R1"
"R2"
"R3"
)   

declare -A runScripts=( 
["R1"]="sbatch startJobs1.sh"
["R2"]="sbatch startJobs2.sh"
["R3"]="sbatch startJobs3.sh"
)

sleep 10s

numJobs=${#jobList[@]}
#echo $numJobs
for ((i=0; i<=$maxtime; i++))
do
    echo " "
    echo "checking at"
    printf '%(%Y-%m-%d %H:%M:%S)T\n' -1
    
    #output=$(bash squeueTest.sh)
    output=$(squeue -u ec-steinboe --format="%.8j")
    jobsRunning=($output)

    #echo "######"
    #echo ${jobsRunning[@]}
    #echo "#####"
    #echo ${jobList[@]}
    #echo "#################"
    needToStart=$(echo ${jobList[@]} ${jobsRunning[@]} | tr ' ' '\n' | sort | uniq -u)
    #echo $needToStart
    
    echo "Need to start:"
    for job in $needToStart
    do
        echo $job
        ${runScripts[${job}]} 
    done
    sleep 7m
    rm slurm-*
done
