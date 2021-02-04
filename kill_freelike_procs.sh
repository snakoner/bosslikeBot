#! /bin/bash

var=$(ps aux | grep "freelike")
uname=$(id -un)
arr=(${var// / }])
arr_len=${#arr[@]}
for ((i=0;i<$arr_len;i++))
do
	if [[ "${arr[$i]}" == $uname ]]; then
		pid=${arr[$i+1]}
		kill -9 $pid
	fi	
done