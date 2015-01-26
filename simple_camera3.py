#!/usr/bin/env python
from __future__ import division, print_function


import datetime
import os
import sys
import time

import picamera


_current_directory = os.path.dirname(os.path.abspath(__file__))
_preview_directory =  "/mnt/ramdisk/previews"
_movie_directory = _current_directory + "/movies"
_start_time = datetime.datetime.now()


def free_space():
    "Free disk space in gigabytes."
    s = os.statvfs('/')
    return (s.f_bavail * s.f_frsize) / 1.0e9


def run():
    if not os.path.exists(_preview_directory):
        os.makedirs(_preview_directory)
    if not os.path.exists(_movie_directory):
        os.makedirs(_movie_directory)
    counter = 1
    with picamera.PiCamera() as camera:
        camera.resolution = (1296, 972) #2592, 1944
        camera.vflip = True
        camera.hflip = True
        camera.start_preview()
        time.sleep(2)
        start_time = datetime.datetime.now()
        try:
            while True:
                timestamp = datetime.datetime.now()
                camera.capture(os.path.join(_preview_directory, "preview.jpg"))
                print("\r{:78}".format(""), end="\r")
                print("\rrunning:{} previews:{}".format(str(timestamp - start_time).split(".")[0], counter), end="")
                sys.stdout.flush()
                counter += 1
                time.sleep(10)
        finally:
                camera.stop_preview()
                camera.close()

if __name__ == "__main__":
    run()
