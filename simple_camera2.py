#!/usr/bin/env python
from __future__ import division, print_function


import datetime
import os
import sys

import picamera


_current_directory = os.path.dirname(os.path.abspath(__file__))
_preview_directory =  "/mnt/ramdisk/previews"
_movie_directory = _current_directory + "/movies"
_resoultion = (1920, 1080)
_preview_resolution = (960, 540)
_framerate = 4 #frames per second
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
        camera.resolution = _resolution
        camera.vflip = True
        camera.hflip = True
        camera.framerate = _framerate
        camera.start_preview()
        try:
            start_time = datetime.datetime.now()
            camera.start_recording(os.path.join(_movie_directory,
                "{}.h264".format(start_time.strftime("%Y%b%d_%H-%M-%S").lower())))
            while free_space() > 0.5:
                timestamp = datetime.datetime.now()
                camera.capture(os.path.join(_preview_directory, "preview.jpg"),
                    resize=_preview_resolution,
                    quality=30,
                    use_video_port=True)
                print("\r{:78}".format(""), end="\r")
                print("\rrunning:{} previews:{}".format(str(timestamp - start_time).split(".")[0], counter), end="")
                sys.stdout.flush()
                counter += 1
                camera.wait_recording(5)

        finally:
            camera.stop_recording()

if __name__ == "__main__":
    run()
