#!/usr/bin/env python3

# monitor.py (c) 2023 Daniel Dowse

import json
import time
import re
import sys
import os
import smtplib, ssl

# Import config for mailserver
import config

matches = []
start = time.time()

# Follow the logfile like tail -f.
def follow(f):
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


# Load keywords from file f
def load_bl(f):
    if os.path.exists(f):
        with open(f, "r") as blacklist:
            words = blacklist.readlines()
            return words
    else:
        with open(f,"w") as blacklist:
            blacklist.write("")
            load_bl(f)

# Find match in url_path for word
def search(url_path, word):
     return re.search(word.strip(), url_path)

# Append to list until timelimit reached
def report(t,data,query):
     global start
     if ( time.time() - start ) < t:
        data["query"] = query
        matches.append(data)
     else:
        data["query"] = query
        matches.append(data)
        report = []
        rows = json.loads(json.dumps(matches))
        for k in json.loads(json.dumps(matches)):
            match = k.get('timestamp'), "Matchword was", '"', k.get('query'), '"', "from", k.get('Hostname'), "MAC:", k.get('MAC') 
            report.append(' '.join(match))
        message = '\n'.join(report)
        # Send mail and flush list
        print("Sending Mail:",text)
        sendmail(config.smtp_server,config.port,config.sender,config.recipient,config.password,message)
        del report[:]

        # Reset timer and clear list
        start = time.time()
        del matches[:]
   
def sendmail(smtp_server,port,csender,recipient,password,message):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

if __name__ == '__main__':
    #with open("/var/log/squid/access.log", "r") as logfile:
    with open(config.squid_log) as logfile:
        while True:
            loglines = follow(logfile)
            #with open("/var/log/monitor.log","a") as monitorlog:
            with open(config.monitor_log,"a") as monitorlog:
                for line in loglines:
                    # Load the latest line
                    data = json.loads(line)
                    path = data.get('Path')
                    # Execute the blacklist function
                    #words = load_bl("/usr/local/etc/squid/acl/monitor")
                    words = load_bl(config.acl_file)
                    for x in words:
                        # Execute the search function
                        query = search(path,x)
                        # Did our query return a match?
                        if query is not None:
                            # Check every N seconds for sending report 
                            report(config.intervall,data,query.group())
                            # Write entry to our logfile
                            print(data.get('timestamp'),"Match was", query.group(), "from client:", data.get('Hostname'), file=monitorlog)
                            # Output to tty if run in terminal 
                            if sys.stdout.isatty():
                              print(data.get('timestamp'),"Match was", query.group(), "from client:", data.get('Hostname'))

# vim: ts=4 sts=4 sw=4 tw=79 expandtab autoindent fileformat=unix
