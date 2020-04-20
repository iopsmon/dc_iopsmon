#DESCRIPTION:This python script pings target servers and writes the output to a csv file, ready for splunk inputs 
#FILENAME:dc_ping_server_0.4.py
#USAGE:python <script name>
#DATE:22/03/2020
#VERSION:0.4
#OWNER:Deepak Chohan

import socket
import os
import csv
import subprocess
import datetime
import time

#Logging Config
#date = {logging.basicConfig (format='%(asctime)s %(message)s', datefmt='%b %d %I:%M:%S')}

#Time variable for how long script took to run
start_time = time.time()

#Message 
print("\033[1;32;40m =================  Starting Ping Test =================  \n")

#Date Format 
MyDate = datetime.datetime.now()
print(MyDate.strftime("%d %m %Y %H:%M:%S")) 


name = {}
CI = {}
hostname = {}
status = {}


#Linux path to servers list file
#myfile = open('../data/servers.csv')     # Mac and Linux
#mytxt = myfile.read()
 #myfile.close()


#Write Headers to csv file 
with open('/opt/splunk/etc/apps/DC_iops_monitoring/data/output_status.csv', 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(["date","server_name","short_name","status","ip_address"]) 

#Read server list in csv file and create a dictionary - the name is CI_Name, then ping the server
# And check status and ip information and write to csv file  
with open('/opt/splunk/etc/apps/DC_iops_monitoring/lookups/servers.csv', 'r', newline='') as csvinput:
#with open('myfile', 'r', newline='') as csvinput:
    reader = csv.DictReader(csvinput)
    for rows in reader:
        CI = rows['CI_Name']
        try:
            ip = socket.gethostbyname(CI)
        except socket.error:
            pass
        name = socket.getfqdn(CI)
        data = name
        hostname = rows['CI_Name']
        response = subprocess.Popen(['/bin/ping', '-c', '3',hostname], stdout = subprocess.PIPE).communicate()[0]
        response = response.decode()
        print(response)
        if '64 bytes' in response:
            status = 'Up'
        elif 'Destination Host Unreachable' in response:
            status = 'Unreachable'
        else:
            status = 'Down'
        if status == 'Down':
            ip = 'Not Found'
        with open('/opt/splunk/etc/apps/DC_iops_monitoring/data/output_status.csv', 'a', newline='') as csvoutput:
            output = csv.writer(csvoutput)
            output.writerow([MyDate.strftime("%d %m %Y %H:%M:%S")] + [hostname] + [data] + [status] + [ip])

#How long script took to run 
print("--- Seconds %s  ---" % (time.time() - start_time))

print("\033[1;32;40m ================= Completed Ping Test =================   \n")



#End of Script 
