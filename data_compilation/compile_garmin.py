#!/usr/bin/env python

import json, datetime, time, sys, os, calendar, shutil, compile_gpx
from housepy import config, log, drawing, science, util, osc, crashdb
from xml.etree import ElementTree
    
MEDIA_LENGTH = 2090.43 # hack per video to get everything to match correctly

log.info("Starting...")

if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
    print("[data_folder]")
    exit()

directory = sys.argv[1]
gpx_filename = None
tcx_filename = None
for filename in os.listdir(directory):
    if filename[-4:] == ".gpx":
        gpx_filename = os.path.join(directory, filename)
    if filename[-4:] == ".tcx":
        tcx_filename = os.path.join(directory, filename)

log.info("GPX %s" % gpx_filename)
log.info("TCX %s" % tcx_filename)

# get video times
video_start_t, video_end_t = compile_gpx.get_video_times(gpx_filename)

# get TCX file
tcx = open(tcx_filename)        
try:
    xml = ElementTree.fromstring(tcx.read())
except Exception, e:
    log.error("XML error (%s): %s" % (tcx_filename, e))
    exit()

# load TCX data
start_t = None
ts = []
heartrates = []
cadences = []
ns = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
trackpoints = xml.findall("%sActivities/%sActivity/%sLap/%sTrack/%sTrackpoint" % tuple([ns]*5))
for trackpoint in trackpoints:
    tstr = trackpoint.findtext("%sTime" % ns)
    dt = datetime.datetime.strptime(tstr, "%Y-%m-%dT%H:%M:%SZ")
    t = float(calendar.timegm(dt.timetuple()))
    t -= 4  # sensor latency
    if t < video_start_t:
        continue
    if t > video_start_t + MEDIA_LENGTH:
        continue
    if start_t is None:
        start_t = t
        t = 0.0
    else:
        t -= start_t
    ts.append(t)
    try:
        heartrate = float(trackpoint.findtext("%sHeartRateBpm/%sValue" % tuple([ns]*2)))
    except Exception:
        heartrate = heartrates[-1] if len(heartrates) else 0.0  # carry over, heartrate doesnt go to 0 (hopefully)
    heartrates.append(heartrate)
    try:
        cadence = float(trackpoint.findtext("%sCadence" % tuple([ns])))
    except Exception as e:
        cadence = 0.0   # drop to 0, probably stopped
    cadences.append(cadence * 2)    # two feet!
log.info("DATA START TIME %s UTC" % datetime.datetime.utcfromtimestamp(start_t).strftime("%Y-%m-%d %H:%M:%S"))
num_samples = len(ts)
log.info("NUM DATA SAMPLES %s" % num_samples)
if len(ts) != int(ts[-1]):
    log.warning("%s != %s" % (util.format_time(len(ts)), util.format_time(ts[-1])))
log.info("DURATION %s" % (util.format_time(ts[-1])))

log.info("CONVERTING AND SAMPLING")

# clean data
cadences = science.filter_deviations(cadences, positive_only=True)
# heartrates = science.filter_deviations(heartrates)

# normalize data
cadences_norm = science.normalize(cadences)
heartrates_norm = science.normalize(heartrates)

# show
ctx = drawing.Context(2000, 250, relative=True, flip=True)
ctx.line([(float(i) / num_samples, cadences_norm[i]) for i in xrange(num_samples)], stroke=(0, 0, 255), thickness=2)
ctx.line([(float(i) / num_samples, heartrates_norm[i]) for i in xrange(num_samples)], stroke=(255, 0, 0), thickness=2)
ctx.show()
ctx.image.save("cadence_heartrate.png", 'PNG')


def rate_to_pulse(signal, sample_rate=60):
    """ Given a rate signal, convert into a list of pulse times. Sample rates in hz. """
    """ Assuming the initial signal is 1hz """
    sample_rate = float(sample_rate)
    elapsed_time = 0.0
    delta = 0.0
    pulses = []
    for i in xrange(len(signal) * int(sample_rate)):
        rate = signal[int(i / sample_rate)] # bpm
        rate /= 60.0  # bps
        if rate > 0:
            period = 1.0 / rate # spb    
            if delta >= period:
                pulses.append(elapsed_time)
                delta = 0.0
        delta += 1.0 / sample_rate
        elapsed_time += 1.0 / sample_rate
    return pulses


log.info("SAVING")

db = crashdb.load("data.json")
db['pedals'] = rate_to_pulse(cadences)
db['heartbeats'] = rate_to_pulse(heartrates)
db.close()

