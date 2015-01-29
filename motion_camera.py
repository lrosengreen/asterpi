#!/usr/bin/env python
from __future__ import division, print_function

# AsterPi v0 copyright (c) 2013-2015 Lars Rosengreen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import copy
import datetime
import multiprocessing
import os
import StringIO
import subprocess
import sys
import time

import numpy

from PIL import Image



_current_directory = os.path.dirname(os.path.abspath(__file__))
_event_directory =  _current_directory + "/events"
_preview_directory = _current_directory + "/previews"
_image_width = 2592
_image_height = 1944
_preview_width = _image_width // 3
_preview_heigh = _image_height // 3
_heartbeat = 100
_darkness_cutoff = 4000000
_darkness_sleeptime = 30 # time in minutes



class Picture:
    def __init__(self, image, timestamp):
        self.image = image
        self.timestamp = timestamp



class RPiCamera:
    def __init__(self, image_size = (_image_width, _image_height)):
        self.image_size = image_size
        self.image_height = image_height
        self.image_counter = 0
        self.start_time = datetime.datetime.now()

    def take_picture(self):
        command = "raspistill -n -mm average -w {} -h {} -ISO 200 -q 100 -t 1000 -e bmp -o -".format(self.image_width, self.image_height)
        image_data = StringIO.StringIO()
        image_data.write(subprocess.check_output(command, shell=True))
        image_data.seek(0)
        image = Image.open(image_data)
        image.load()
        image_data.close()
        timestamp = datetime.datetime.now()
        picture = Picture(image, timestamp)
        self.image_counter += 1
        return picture

class DummyCamera:
    def __init__(self, image_size=(_image_width, _image_height)):
        self.image_size = image_size
        self.image_counter = 0
        self.start_time = datetime.datetime.now()
        self.running = False

    def start(self):
        self.running = True
        time.sleep(10)

    def stop(self):
        self.running = False

    def take_picture(self):
        # start up the camera if it is not currently running
        if not self.running: self.start()
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        image = Image.new('RGB', self.image_size, color)
        timestamp = datetime.datetime.now()
        self.image_counter += 1
        time.sleep(2)
        return (image, timestamp)




def brightness(picture):
    m = numpy.asarray(picture.image)
    return numpy.sum(m)


def save_picture(picture, counter):
    outfile = "{:05d}_{}.jpg".format(counter,
                picture.timestamp.strftime("%Y%b%d_%H%M%S"))
    image = picture.image
    preview = image.resize((_preview_width,_preview_heigh))
    preview.save(os.path.join(_preview_directory, outfile))
    image.save(os.path.join(_event_directory, outfile), quality=90)


def free_space():
    "Free disk space in gigabytes."
    s = os.statvfs('/')
    return (s.f_bavail * s.f_frsize) / 1.0e9


def report_status(message, queue=None):
    print("\r{:78}".format(""), end="\r")
    print("\r" + message, end="")
    sys.stdout.flush()
    if queue is not None:
        while not queue.empty():
            queue.get()
        queue.put(message)





def run(queue=None):
    if not os.path.exists(_event_directory):
        os.makedirs(_event_directory)
    if not os.path.exists(_preview_directory):
        os.makedirs(_preview_directory)

    Camera = RPiCamera()

    while True:
        picture = Camera.take_picture()
        running_time = str(picture.timestamp - Camera.start_time).split('.')[0]
        report_status("time: {} images: {}".format(running_time, Camera.image_counter), queue)
        save_picture(picture, Camera.image_counter)




if __name__ == "__main__":
    run()
