#! /bin/bash

var=$(ps aux | grep "bosslike")
echo $var
arr=(${var// / }])
arr_len=${#arr[@]}
for ((i=0;i<$arr_len;i++))
do
	if [[ "${arr[$i]}" == "andryusha" ]]; then
		pid=${arr[$i+1]}
		echo $pid
		kill -9 $pid
	fi	
done