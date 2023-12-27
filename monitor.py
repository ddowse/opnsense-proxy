# monitor.py (c) 2023 Daniel Dowse

import json
import time
import re
import sys
import os

# Follow the logfile like tail -f.
def follow(f):
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


# Load keywords from file
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

def search(url_path, word):
     return re.search(word.strip(), url_path)


if __name__ == '__main__':
    with open("/var/log/squid/access.log", "r") as logfile:
        while True:
            loglines = follow(logfile)
            with open("/var/log/monitor.log","a") as monitorlog:
                for line in loglines:
                    data = json.loads(line)
                    #print("DEBUG: main() type(data)", type(data))
                    #print("DEBUG: Raw data:", data)
                    path = data.get('Path')
                    #path = data.get('Path').split('&')
                    words = load_bl("/usr/local/etc/squid/acl/monitor")
                    for x in words:
                        query = search(path,x)
                        if query is not None:
                          print(data.get('timestamp'),"Match was", query.group(), "from client:", data.get('Hostname'), file=monitorlog)
                          if sys.stdout.isatty():
                            print(data.get('timestamp'),"Match was", query.group(), "from client:", data.get('Hostname'))

# vim: ts=4 sts=4 sw=4 tw=79 expandtab autoindent fileformat=unix
