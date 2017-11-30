#!/usr/bin/env python2

import sys
import subprocess

MINICLIENT_BINARY="/usr/bin/miniclient"

args = [MINICLIENT_BINARY]
args = args + sys.argv[1:len(sys.argv)]
print args

subprocess.call(args)

