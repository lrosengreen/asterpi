#!/usr/bin/env python
from __future__ import division, print_function

# AsterPi v0 copyright (c) 2013, 2014 Lars Rosengreen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from multiprocessing import Process, Queue

import motion_camera
import motion_server


__author__ = "Lars Rosengreen"
__email__ = "lars.rosengreen@sjsu.edu"
__license__ = "GPL"
__version__ = "0"


if __name__ == "__main__":
    print("MotionPi v{}".format(__version__))
    queue = Queue()
    p_camera = Process(target=motion_camera.run, args=(queue,))
    p_server = Process(target=motion_server.run, args=(queue,))
    p_camera.start()
    p_server.start()
    p_camera.join()
