#!/usr/bin/env python

import json, datetime, time, sys, os, calendar, shutil
from housepy import config, log, drawing, science, util, osc, crashdb
from xml.etree import ElementTree


def get_video_times(gpx_filename):

    # get GPX file
    gpx = open(gpx_filename)        
    try:
        xml = ElementTree.fromstring(gpx.read())
    except Exception, e:
        log.error("XML error (%s): %s" % (tcx_filename, e))
        exit()

    # load GPX data
    # basically, look at the first GPS time and the corresponding media time, and subtract to get the precise start time
    ns = "{http://www.topografix.com/GPX/1/1}"
    timestamps = xml.findall("%strk/%strkseg/%strkpt/%stime" % tuple([ns]*4))
    first_timestamp = timestamps[0].text
    first_timestamp_dt = datetime.datetime.strptime(first_timestamp, "%Y-%m-%dT%H:%M:%S")
    first_timestamp_t = calendar.timegm(first_timestamp_dt.timetuple())

    media_times = xml.findall("%strk/%strkseg/%strkpt/%sextensions/%smediatime" % tuple([ns]*5))
    first_media_time = media_times[0].text
    first_media_time_dt = time.strptime(first_media_time, "%H:%M:%S.%f")
    first_media_time_seconds = first_media_time_dt.tm_min * 60 + first_media_time_dt.tm_sec
    start_timestamp = first_timestamp_t - first_media_time_seconds
    end_timestamp = timestamps[-1].text
    video_start_dt = datetime.datetime.utcfromtimestamp(start_timestamp)
    video_start_t = float(calendar.timegm(video_start_dt.timetuple()))
    video_end_dt = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%S")
    video_end_t = float(calendar.timegm(video_end_dt.timetuple()))
    log.info("VIDEO START REAL TIME %s UTC" % datetime.datetime.utcfromtimestamp(video_start_t).strftime("%Y-%m-%d %H:%M:%S"))
    log.info("VIDEO END REAL TIME %s UTC" % datetime.datetime.utcfromtimestamp(video_end_t).strftime("%Y-%m-%d %H:%M:%S"))

    return video_start_t, video_end_t       ## note! this is just the last GPS point, not necessarily the end of the movie!