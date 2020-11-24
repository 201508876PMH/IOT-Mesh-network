timestamp(){
 echo $(date "+%Y/%m/%d-%H:%M:%S") #current time
}



counter=0
while true
	do
	sleep 1
	timevariable=$(timestamp)
	counter=$(($counter+1))
	echo "Current timestamp: " $timevariable > logfile_node04.txt
	echo "Number of file iterations: " $counter >> logfile_node04.txt
        echo "" >> logfile_node04.txt
	meshmerize neighbor >> logfile_node04.txt
	echo "" >> logfile_node04.txt
	meshmerize originator >> logfile_node04.txt

        scp logfile_node_04.txt root@10.1.0.1:/root/logfiles
done


