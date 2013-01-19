#!/usr/bin/env python

import json, datetime, time, sys, os, random, math
from housepy import config, log, util, osc, crashdb
from helpers.notation import *
from helpers.tweens import *


CHORDS = [  (A2, B3, G5),
            (G2, B3, A5),
            (F2, C, A5),
            (F2, D, G5),
            (E2, D, B5),
            (F2, C, B5),
            (F2, B3, A5),
            (A2, B3, G5)
            ]

db = crashdb.load("data.json")

max_t = max(((max(db['heartbeats'][-1], db['pedals'][-1])), db['breaths'][-1]))
log.info("MAX TIME %s" % util.format_time(max_t))

notes = []

for heartbeat in db['heartbeats']:
    pos = heartbeat / max_t
    chord_pos = pos * (len(CHORDS) - 1)
    p1, p2 = CHORDS[int(math.floor(chord_pos))][0], CHORDS[int(math.ceil(chord_pos))][0]    
    chord_pos -= int(chord_pos)
    chord_pos = ease_in_out(chord_pos)
    pitch = p1 if random.random() > chord_pos else p2
    notes.append((heartbeat, [1, pitch, 127, util.format_time(heartbeat), chord_pos, p1, p2, get_note_name(pitch)]))
    # notes.append((heartbeat + 0.1, [HEARTBEAT_CHANNEL, pitch, 110, util.format_time(heartbeat)]))

for pedal in db['pedals']:
    pos = pedal / max_t
    chord_pos = pos * (len(CHORDS) - 1)
    p1, p2 = CHORDS[int(math.floor(chord_pos))][1], CHORDS[int(math.ceil(chord_pos))][1]    
    chord_pos -= int(chord_pos)  
    chord_pos = ease_in_out(chord_pos)  
    pitch = p1 if random.random() > chord_pos else p2
    notes.append((pedal, [2, pitch, 127, util.format_time(pedal), chord_pos, p1, p2, get_note_name(pitch)]))

for breath in db['breaths']:
    pos = breath / max_t
    chord_pos = pos * (len(CHORDS) - 1)
    p1, p2 = CHORDS[int(math.floor(chord_pos))][2], CHORDS[int(math.ceil(chord_pos))][2]
    chord_pos -= int(chord_pos)    
    chord_pos = ease_in_out(chord_pos)
    pitch = p1 if random.random() > chord_pos else p2
    notes.append((breath, [3, pitch, 127, util.format_time(breath), chord_pos, p1, p2, get_note_name(pitch)]))

notes.sort(key=lambda n: n[0])
db['notes'] = notes
db.close()