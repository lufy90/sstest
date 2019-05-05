#!/bin/bash
# stress.sh

# stress system with stress command.
# Usage:
# ./stress 200    -- loop running stressing for 30s, 200s in total.
# Auto generate a sar log in ./sar_<timestamp>.log

cpus=8
mem=32000
swap=8191
t=$1
D=`date +%Y%m%d%H%M%S`


sleep $t &
sleep_pid=$!

sar -A 5 -o sar_${D}.log > /dev/null &
sar_pid=$!

while [[ $(ps -p $sleep_pid -o comm=) == "sleep" ]]
do
echo $(date) "Start stress ... "
stress -c $cpus -i $cpus -m $cpus --vm-bytes ${mem}M -t 30 -v
echo "End stress"
done

kill -9 $sar_pid

