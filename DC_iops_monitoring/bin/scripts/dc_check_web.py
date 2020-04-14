#DESCRIPTION:This python script monitors web sites  
#FILENAME:
#USAGE:python <script name>
#DATE:28/03/2020
#VERSION:0.1
#OWNER:Deepak Chohan
 
#import modules
import urllib.request
import datetime
import os
import sys
import datetime
import time 

#custom variables
#Time 
my_date = datetime.datetime.now()

#Agent String - Required for some sites - not used here - ony for ref
user_agent_string = "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/74.0" 

#Path Ref
#urlfile_name =  os.path.join(os.environ["SPLUNK_HOME"], 'etc', 'apps', TA, 'config', urlfile_name_txt)


def my_url_check():
        #Local variables (custom log files)
        url_cfg_file = ("/opt/splunk/etc/apps/DC_iops_monitoring/bin/scripts/url.conf")
        up_status_file = datetime.datetime.now().strftime("/opt/splunk/etc/apps/DC_iops_monitoring/bin/scripts/logs/"'%H_%M_%d_%m_%Y.%f_up_status.log') 
        down_status_file = datetime.datetime.now().strftime("/opt/splunk/etc/apps/DC_iops_monitoring/bin/scripts/logs/"'%H_%M_%d_%m_%Y.%f_down_status.log')
        time.sleep(2)
        #Create new files 
        my_down_f = open(down_status_file, "x+")
        my_up_f = open(up_status_file, "x+")
        time.sleep(1)

        #custom url_file 
        url_file = open(url_cfg_file, "r")
        #Main Code - check URL, if error connecting, log to down file, else log to up file
        for my_url in url_file:
            try: 
               urllib.request.urlopen(my_url, timeout=15)
            except urllib.error.HTTPError as e:
                print(e.code)
                print(e.read())  
                print('Server Page Not Found', my_url) 
                my_down_f = open(down_status_file, "a")
                my_down_f.write(my_date.strftime("%d %m %Y %H:%M:%S"))
                my_down_f.write(" code=404")
                my_down_f.write(" down=")
                my_down_f.write(my_url)
                time.sleep(1)
            else:       
                print('Server Page Found', my_url) 
                my_up_f = open(up_status_file, "a")
                my_up_f.write(my_date.strftime("%d %m %Y %H:%M:%S"))
                my_up_f.write(" code=200")
                my_up_f.write(" up=")
                my_up_f.write(my_url)
                time.sleep(1)
                               
           
        
#Call Functions 
my_url_check() 


