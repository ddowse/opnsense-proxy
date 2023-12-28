# Parental Monitor

## What is this... 

This is a tool that reads the ```access.log``` of Squid Proxy continuously.   
It will check the URL part of each new logline for matching patterns specified   
in a ACL file and records the match to a local logfile. The logfile with all   
matches will be send as plain text email to a configurable destination.    

## Prepare your OPNsense installation 

### Step 1
Go and visit the OPNsense Documentation and setup a transparent proxy.

https://docs.opnsense.org/manual/how-tos/proxytransparent.html

### Step 2 
Download the CA Certificate and distribute it to your devices.   
In most cases a "double click" on the File will trigger a import dialog   
from your OS.    

https://docs.opnsense.org/manual/how-tos/proxytransparent.html#step-4-ca-for-transparent-ssl   


## Install this software 

### Step 1

Login to your OPNsense via SSH and clone or download this repo. 

```
cd opnsense-proxy
./install-and-patch.sh
```

### Step 2

Configure SMTP by editing ```/usr/local/etc/parental-monitor-config.py```

### Step 3

Add keywords that you want to report on in this file

``` /usr/local/etc/squid/acl/monitor ```

by editing it in the shell with your favourite editor or edit it somewhere   
else and copy it to the path via e.g ```scp``` from the remote site.   

### Step 4

Start the script and monitor the logfile for matches and recieve them via email.   

``` 
configctl parental-monitor start
```


