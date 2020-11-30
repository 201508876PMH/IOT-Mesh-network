timestamp(){
 echo $(date "+%Y/%m/%d-%H:%M:%S") #current time
}

getIPAddr(){
 echo $(ifconfig | grep -E -o 'inet addr:10.1.0.\d')
}

counter=0
while true
	do
	 timevariable=$(timestamp)
	 IPAddr=$(getIPAddr)
	 counter=$(($counter+1))
	 echo "IP.addr: " $IPAddr > /root/logfiles/logfile_node01_NR.txt
	 echo "Current timestamp: " $timevariable >> /root/logfiles/logfile_node01_NR.txt
	 echo "Number of file iterations: " $counter >> /root/logfiles/logfile_node01_NR.txt
	 echo "" >> /root/logfiles/logfile_node01_NR.txt
	 meshmerize neighbor >> /root/logfiles/logfile_node01_NR.txt
	 echo "" >> /root/logfiles/logfile_node01_NR.txt
	 meshmerize originator >> /root/logfiles/logfile_node01_NR.txt
	 mv /root/logfiles/logfile_node01_NR.txt /root/logfiles/logfile_node01.txt
	 sleep 1
	
done


