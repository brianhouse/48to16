#!/usr/bin/env python3

import json, datetime, time, sys, os, random, math, os, sys
from housepy import config, log, util, osc, process

""" For use instead of sync + maxpatch, ie, videoless version """

process.secure_pid(os.path.join(os.path.dirname(__file__), "run"))

if len(sys.argv) > 1:
    skip = float(sys.argv[1]) * 60  # argument in minutes
else:
    skip = 0.0

sender = osc.Sender()

for player in config['players']:
    sender.add_target(player['ip'], player['port'])

start_t = time.time()
start_t -= skip
updated = False
while True:
    t = time.time() - start_t
    if int(t % 5) == 0:
        if not updated:
            sender.send("/sync", t)
            updated = True
    else:
        updated = False
    time.sleep(0.1)

