#!/usr/bin/python

import re
import os


#----------------------------------------------------------------------------------------------------------
lifeline = re.compile(r"(\d) received")
def ping(host):
    cmd = os.popen("ping -q -c2 -i0.7 -W 1 " + host, "r")
    while 1:
        line = cmd.readline()
        if not line: break
        igot = re.findall(lifeline, line)
        if igot:
            return {host: int(igot[0])}


