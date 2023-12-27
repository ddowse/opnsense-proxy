# monitor.py (c) 2023 Daniel Dowse

import json
import time
import re
import sys
import os
import mail

matches = []

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
            # Return a list of all words found in the file separated by newlines
            return words
    else:
        with open(f,"w") as blacklist:
            blacklist.write("")
            load_bl(f)

# Find match in url_path for word
def search(url_path, word):
     return re.search(word.strip(), url_path)

# Append to list until limit reached
def limit(l,data,query):
     if len(matches) < l:
            data["query"] = query
            matches.append(data)
     else:
        rows = []
        # Send mail and flush list
        report = json.loads(json.dumps(matches))
        for k in report:
            row = k.get('timestamp'), "Matchword was", '"', k.get('query'), '"', "from", k.get('Hostname'), "MAC:", k.get('MAC') 
            rows.append(' '.join(row))
        
        mail.text = '\n'.join(rows)
        mail.send()
        del matches[:]

if __name__ == '__main__':
    with open("/var/log/squid/access.log", "r") as logfile:
        while True:
            loglines = follow(logfile)
            with open("/var/log/monitor.log","a") as monitorlog:
                for line in loglines:
                    # Load the latest line
                    data = json.loads(line)
                    path = data.get('Path')
                    # Execute the blacklist function
                    words = load_bl("/usr/local/etc/squid/acl/monitor")
                    for x in words:
                        # Execute the search function
                        query = search(path,x)
                        # Did our query return a match?
                        if query is not None:
                            # Send every N lines
                            limit(100,data,query.group())
                            # Write entry to our logfile
                            print(data.get('timestamp'),"Match was", query.group(), "from client:", data.get('Hostname'), file=monitorlog)
                            # Output to tty if run in terminal 
                            if sys.stdout.isatty():
                              print(data.get('timestamp'),"Match was", query.group(), "from client:", data.get('Hostname'))

# vim: ts=4 sts=4 sw=4 tw=79 expandtab autoindent fileformat=unix
