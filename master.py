#!/usr/bin/env python3

import json, datetime, time, sys, os, random, math
from housepy import config, log, util, osc

""" For use instead of sync + maxpatch, ie, videoless version """

sender = osc.Sender()

for player in config['players']:
    sender.add_target(player['ip'], player['port'])

start_t = time.time()
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

