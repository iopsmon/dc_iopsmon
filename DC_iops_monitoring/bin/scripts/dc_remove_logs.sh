#!/bin/bash

#Deletes old log files


MAX_DAYS_KEEP_LOGS=1


#command to delete logs 
echo "Python scripts are done, looking for log files to clear."
find /opt/splunk/etc/apps/DC_iops_monitoring/bin/scripts/logs/*.log -type f -mtime +$MAX_DAYS_KEEP_LOGS -delete
