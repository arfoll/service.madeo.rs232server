#!/usr/bin/env python3

import os
import sys
import subprocess
import errno

if len(sys.argv) < 3:
    print ("error: Not enough arguments")
    print ("       xbmcclient.py <RS232_SERVICE> <ACTION>")
    print ("   ex: xbmcclient.py azur mute")
    sys.exit(errno.EINVAL)

CLEVERMUTE_LOCK="/tmp/clevermute"
MINICLIENT_BINARY="/usr/bin/miniclient"
RS232_SERVICE=sys.argv[1]
ACTION1=sys.argv[2]
#MUTEVOID=['unmute', 'poweroff', 'voldown', 'volup']

#if ACTION1 in MUTEVOID:
#    try:
#        os.remove(CLEVERMUTE_LOCK)
#    except Exception:
#        pass

if ACTION1 == "clevermute":
    if os.path.exists(CLEVERMUTE_LOCK):
        sys.argv[2]="unmute"
        os.remove(CLEVERMUTE_LOCK)
    else:
        f=open(CLEVERMUTE_LOCK, "w+")
        sys.argv[2]="mute"

args = [MINICLIENT_BINARY] + [RS232_SERVICE] + sys.argv[2:len(sys.argv)]
#print(args)

subprocess.call(args)
sys.exit(0)
