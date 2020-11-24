timestamp(){
 echo $(date "+%Y/%m/%d-%H:%M:%S") #current time
}



counter=0
while true
	do
	sleep 1
	timevariable=$(timestamp)
	counter=$(($counter+1))
	echo "Current timestamp: " $timevariable > /root/logfiles/logfile_node01.txt
	echo "Number of file iterations: " $counter >> /root/logfile/logfile_node01.txt
        echo "" >> /root/logfiles/logfile_node01.txt
	meshmerize neighbor >> /root/logfiles/logfile_node01.txt
	echo "" >> /root/logfiles/logfile_node01.txt
	meshmerize originator >> /root/logfiles/logfile_node01.txt

done


