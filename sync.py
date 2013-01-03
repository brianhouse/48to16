#!/usr/bin/env python

import json, datetime, time, sys, os, random, math
from housepy import config, log, util, osc, crashdb

BEGIN = 28 * 60  # min      # gauntlet
BEGIN = 13 * 60  # min      # bridge
BEGIN = 0 * 60
COUNTOFF = 3   # sec
SYNC_FPS = 0.5

db = crashdb.load("data.json")
notes = db['notes']
db.close()

players = []
for ip in config['players']:
    players.append(osc.Sender(ip, 39393))

time.sleep(COUNTOFF)

start = time.time()
start -= BEGIN
last_frame = 0
i = 0
first_frame = True

for player in players:
    player.send("/sync", 0)

while True:
    t = time.time() - start
    if t - last_frame > 1.0 / SYNC_FPS:
        for player in players:
            player.send("/sync", t)
        last_frame = t
    while i < len(notes) and notes[i][0] < t:
        latency = t - notes[i][0]
        if not first_frame and abs(latency * 1000.0) > .9:
            log.warning("latency %fms" % (latency * 1000.0))
        i += 1
    time.sleep(0.0005)
    first_frame = False    
    if i == len(notes):
        break

