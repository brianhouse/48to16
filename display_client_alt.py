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
note_index = 0
t = 0
previous_frame = None
started = False

def message_handler(location, address, data):
    if address == "/sync":
        # t_queue.put(data[0])
        global t
        global started
        t = data[0]
        if not started:
            started = True
        pass
receiver = osc.Receiver(39393, message_handler)

def draw():
    global t
    global previous_frame
    draw_staff()    
    if not started:
        return
    start_frame = time.time()
    if previous_frame is None:
        previous_frame = start_frame
    t += start_frame - previous_frame
    previous_frame = start_frame    
    draw_frame(t)

def draw_staff():
    h = 0.125
    for i in xrange(5):
        i += 2
        ctx.line(0.0, i * h, 1.0, i * h, thickness=2.0)#, color=(1., 1., 1., 1.))    

def draw_frame(t):
    global note_index

    page_num = int(t / page_duration)
    page_pos = (t / page_duration) - page_num
    page_t = page_num * page_duration

    start_index = note_index
    while notes[start_index] < page_t:
        start_index += 1    
    stop_t = page_t + page_duration
    stop_index = start_index + 1
    while notes[stop_index] <= stop_t:
        stop_index += 1

    current_notes = np.array(notes[start_index:stop_index])
    current_note_info = np.array(note_infos[start_index:stop_index])
    current_notes -= page_t
    current_notes /= page_duration

    for i, t in enumerate(current_notes):
        note_info = current_note_info[i]        
        channel = int(note_info[0])
        note = int(note_info[1])        
        vertical = (get_bass_ledger(note) * 0.0625) + 0.0625

        if CHANNEL is not None and channel != CHANNEL:
            continue

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

    ctx.line(page_pos, 0.0, page_pos, 1.0, thickness=2.0)#, color=(1., 1., 1., 1.))    


ctx.start(draw)
