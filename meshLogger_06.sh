timestamp(){
 echo $(date "+%Y/%m/%d-%H:%M:%S") #current time
}



counter=0
while true
	do
	sleep 1
	timevariable=$(timestamp)
	counter=$(($counter+1))
	echo "Current timestamp: " $timevariable > logfile_node06.txt
	echo "Number of file iterations: " $counter >> logfile_node06.txt
        echo "" >> logfile_node06.txt
	meshmerize neighbor >> logfile_node06.txt
	echo "" >> logfile_node06.txt
	meshmerize originator >> logfile_node06.txt

        scp logfile_node_06.txt root@10.1.0.1:/root/logfiles
done


