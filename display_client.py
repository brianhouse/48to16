#!/usr/bin/env python

import json, datetime, time, sys, os, Queue, random, pyglet
from housepy import config, log, util, osc, crashdb, animation
import numpy as np

CHANNEL = None

if len(sys.argv) > 1:
    CHANNEL = int(sys.argv[1])

db = crashdb.load("data.json")
db.close()
note_rows = db['notes']
notes = [nr[0] for nr in note_rows]
note_infos = [nr[1] for nr in note_rows]

ctx = animation.Context(1200, 600, background=(0.9, 0.9, 0.9, 1.), fullscreen=False, title="Forty-eight to Sixteen")

page_duration = 5.0
margin = 1.0
hitpoint = margin / (page_duration - margin)
note_index = 0
start_t = 0
t = 0
last_t = 0
started = False

def message_handler(location, address, data):
    if address == "/sync":
        global t
        global started
        global start_t
        global last_t
        t = data[0]
        if not started:
            started = True
            start_t = time.time()
            last_t = start_t
receiver = osc.Receiver(39393, message_handler)

def draw():
    global t
    global last_t
    draw_staff()    
    if not started:
        return
    start_frame = time.time()
    t += start_frame - last_t
    last_t = start_frame    
    draw_frame(t)
    ctx.line(hitpoint, 0.0, hitpoint, 1.0, thickness=2.0)#, color=(1., 1., 1., 1.))    

def draw_staff():
    h = 0.125
    for i in xrange(5):
        i += 2
        ctx.line(0.0, i * h, 1.0, i * h, thickness=2.0)#, color=(1., 1., 1., 1.))    

def draw_frame(t):
    global note_index
    start_index = note_index
    while notes[start_index] < (t - margin):
        start_index += 1    
    stop_t = (t - margin) + (page_duration - margin)
    stop_index = start_index + 1
    while notes[stop_index] <= stop_t:
        stop_index += 1
    current_notes = np.array(notes[start_index:stop_index])
    current_note_info = np.array(note_infos[start_index:stop_index])
    current_notes -= (t - margin)
    current_notes /= (page_duration - margin)
    for i, t in enumerate(current_notes):
        note_info = current_note_info[i]        
        channel = int(note_info[0])
        note = int(note_info[1])        
        vertical = (get_bass_ledger(note) * 0.0625) + 0.0625

        if CHANNEL is not None and channel != CHANNEL:
            continue

        intensity = 1.0 - abs(hitpoint - t)
        intensity /= 2.0
        if channel == 1:
            color = (.6, 0., 0., 1.)
        elif channel == 2:
            color = (0., .6, 0., 1.)
        elif channel == 3:
            color = (0., 0., .6, 1.)                

        vertical += 0.010
        # vertical += int(str(note_info[4])[-2]) * 0.001
        width = ((0.105 * ctx.height) / ctx.width)
        height = 0.105
        ctx.rect(t, vertical, width, height, color=color, thickness=1.0)
    note_index = start_index

ctx.start(draw)
