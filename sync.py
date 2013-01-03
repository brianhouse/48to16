#!/usr/bin/env python

import json, datetime, time, sys, os, random, math
from housepy import config, log, util, osc

sender = osc.Sender()

for ip in config['players']:
    sender.add_target(ip, 39393)

def message_handler(location, address, data):  
    if address != "/update":
        return
    t = data[0]
    sender.send("/sync", t)

osc.Receiver(23232, message_handler, blocking=True)

