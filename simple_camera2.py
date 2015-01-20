#!/usr/bin/env python
from __future__ import division, print_function


import datetime
import os
import sys

import picamera


_current_directory = os.path.dirname(os.path.abspath(__file__))
_picture_directory =  _current_directory + "/pictures"
_movie_directory = _current_directory + "/movies"
_start_time = datetime.datetime.now()


def free_space():
    "Free disk space in gigabytes."
    s = os.statvfs('/')
    return (s.f_bavail * s.f_frsize) / 1.0e9


def run():
    if not os.path.exists(_picture_directory):
        os.makedirs(_picture_directory)
    if not os.path.exists(_movie_directory):
        os.makedirs(_movie_directory)
    counter = 0
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        camera.vflip = True
        camera.hflip = True
        camera.framerate = 4
        camera.start_preview()
        try:
            start_time = datetime.datetime.now()
            camera.start_recording(os.path.join(_movie_directory,
                "{}.h264".format(start_time.strftime("%Y%b%d_%H%M"))))
            while free_space() > 1:
                camera.wait_recording(10)
                timestamp = datetime.datetime.now()
                camera.capture(os.path.join(_picture_directory,
                    "{:05d} {}.jpg".format(counter, timestamp.strftime("%Y%b%d_%H%M%S"))),
                    resize=(960,540), use_video_port=True)
                print("\r{:78}".format(""), end="\r")
                print("\revents: {}".format(counter), end="")
                sys.stdout.flush()
                counter = counter + 1

        finally:
            camera.stop_recording()

if __name__ == "__main__":
    run()
