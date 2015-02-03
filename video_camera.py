#!/usr/bin/env python
from __future__ import division, print_function


import datetime
import io
import os
import sys
import time

import numpy
import picamera

from PIL import Image


_current_directory = os.path.dirname(os.path.abspath(__file__))
_preview_directory =  "/mnt/ramdisk/previews"
_movie_directory = _current_directory + "/movies"
_resolution = (1920, 1080)
_preview_resolution = (960, 540)
_framerate = 4 #frames per second
_start_time = datetime.time(7) # start time in hours (24 hr clock)
_end_time = datetime.time(17) # end time in hours (24hr clock)
_minimum_free_space = 0.5 #stop if free space gets lower than this in GB

def brightness(image):
    m = numpy.asarray(image)
    return numpy.sum(m)


def free_space():
    "Free disk space in gigabytes."
    s = os.statvfs('/')
    return (s.f_bavail * s.f_frsize) / 1.0e9


def run():
    if not os.path.exists(_preview_directory):
        os.makedirs(_preview_directory)
    if not os.path.exists(_movie_directory):
        os.makedirs(_movie_directory)

    now = datetime.datetime.now().time()
    while free_space() > _minimum_free_space:
        now = datetime.datetime.now().time()
        if now > _start_time and now < _end_time:
            counter = 1
            with picamera.PiCamera() as camera:
                camera.resolution = _resolution
                camera.vflip = True
                camera.hflip = True
                camera.framerate = _framerate
                camera.annotate_background = True
                try:
                    start_time = datetime.datetime.now()
                    fname = os.path.join(_movie_directory, "{}.h264".format(start_time.strftime("%Y%b%d_%H-%M-%S").lower()))
                    print("recording to {}".format(fname))
                    camera.start_recording(fname)
                    while free_space() > _minimum_free_space and now > _start_time and now < _end_time:
                        timestamp = datetime.datetime.now()
                        now = timestamp.time()
                        camera.annotate_text = timestamp.strftime("%Y%b%d %H:%M").lower()
                        camera.capture(os.path.join(_preview_directory,"preview.jpg"),
                                resize=_preview_resolution,
                                quality=30,
                                use_video_port=True)
                        print("\r{:78}".format(""), end="\r")
                        print("\rrunning:{} previews:{}".format(str(timestamp - start_time).split(".")[0], counter), end="")
                        sys.stdout.flush()
                        counter += 1
                        camera.wait_recording(60)
                finally:
                    camera.stop_recording()
        else:
            print("\r{:78}".format(""), end="\r")
            print("\rwaiting until: {} ({})".format(str(_start_time), str(now).split(".")[0]), end="")
            sys.stdout.flush()
            time.sleep(20)


if __name__ == "__main__":
    run()
