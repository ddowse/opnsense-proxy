# monitor.py

import json
import time
import re


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
    with open(f, "r") as blacklist:
        words = blacklist.readlines()
        # Return a list of all words found in the file separated by newlines
        return words


def search(url_path, word):
#    print("DEBUG: search() ")
#    print("DEBUG: search() Path (url_path):", url_path)
#    print("DEBUG: search() Blacklist (word):", (word.strip()))
#    print("DEBUG: search() RegEx:", re.search(word.strip(), url_path))
     return re.search(word.strip(), url_path)

if __name__ == '__main__':
    with open("/var/log/squid/access.log", "r") as logfile:
        while True:
            loglines = follow(logfile)
            for line in loglines:
                data = json.loads(line)
                #print("DEBUG: main() type(data)", type(data))
                #print("DEBUG: Raw data:", data)
                path = data.get('Path')
                #path = data.get('Path').split('&')
                words = load_bl("./blacklist")
                for x in words:
                    query = search(path,x)
                    if query is not None:
                      print("Match was", query.group())
