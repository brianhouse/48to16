#!/usr/bin/env python3

import json, datetime, time, sys, os, random, math
from housepy import config, log, util, osc

sender = osc.Sender()

for player in config['players']:
    sender.add_target(player['ip'], player['port'])

def message_handler(location, address, data):  
    if address != "/update":
        return
    t = data[0]
    t += config['latency']
    sender.send("/sync", t)

osc.Receiver(23232, message_handler, blocking=True)

