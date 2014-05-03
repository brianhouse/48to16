#!/usr/bin/env python3

import sys, os, datetime, calendar, compile_gpx, pytz
import numpy as np
from scipy.io import wavfile
from housepy import log, config, util, drawing, science, crashdb

MEDIA_LENGTH = 2090.43 # hack per video to get everything to match correctly

log.info("Starting...")

if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
    print("[data_folder]")
    exit()

directory = sys.argv[1]
gpx_filename = None
wav_filename = None
for filename in os.listdir(directory):
    if filename[-4:] == ".gpx":
        gpx_filename = os.path.join(directory, filename)    
    if filename[-4:] == ".wav":
        wav_filename = os.path.join(directory, filename)

log.info("GPX %s" % gpx_filename)
log.info("WAV %s" % wav_filename)

audio_start_dt = datetime.datetime.strptime(wav_filename.split('.')[0].split('/')[-1].replace('_smp', ''), "%Y%m%d %H%M%S")
audio_start_dt = util.to_utc(audio_start_dt)

# get video times
video_start_t, video_end_t = compile_gpx.get_video_times(gpx_filename)

log.info("AUDIO START %s" %  audio_start_dt)
audio_start_t = float(calendar.timegm(audio_start_dt.timetuple()))
sample_rate, data = wavfile.read(wav_filename)
log.info("AUDIO SAMPLE RATE %s" % sample_rate)
log.info("AUDIO LENGTH (samples) %s" % len(data))
seconds = float(len(data)) / sample_rate
log.info("AUDIO DURATION %s" % util.format_time(seconds))
skip = video_start_t - audio_start_t
log.info("AUDIO SKIP %s%s" % ('-' if skip < 0 else '', util.format_time(abs(skip))))

# downsample to 60hz
target_sample_rate = 60.0
signal = science.downsample(data, int(sample_rate / target_sample_rate))
log.info("NEW LENGTH (samples) %s" % len(signal))
average = np.average(signal)
reduced = signal - average
reduced = [x if x >= 0 else 0 for x in reduced]
reduced = science.smooth(reduced, window_len=50)
reduced = science.normalize(reduced)
signal = science.normalize(signal)

log.info("DETECTING PEAKS")
# the lookahead is key. dont want to see two peaks, but not too small
# in this case, a breath a second?
max_peaks, min_peaks = science.detect_peaks(reduced, lookahead=60)
breaths = []
for peak in max_peaks:
    sample, y = peak
    t = sample / target_sample_rate
    t -= skip
    if t < 0:
        continue
    if t > MEDIA_LENGTH:
        continue
    breaths.append(t)

log.info("SAVING")
db = crashdb.load("data.json")
db['breaths'] = breaths
db.close()


num_samples = len(signal)
ctx = drawing.Context(10000, 500, relative=True, flip=True, hsv=True)
ctx.line([(float(i) / num_samples, signal[i]) for i in range(num_samples)], stroke=(0., 0., 0.85), thickness=2)
ctx.line([(float(i) / num_samples, reduced[i]) for i in range(num_samples)], stroke=(0.55, 1., 1.), thickness=2)
for peak in max_peaks:
    sample, y = peak
    ctx.arc(float(sample) / num_samples, y, 5. / ctx.width, 5. / ctx.height, thickness=0., fill=(0., 1., 1.))
ctx.show()
ctx.image.save("breaths.png", 'PNG')


