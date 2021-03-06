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


import json
import os
import os.path

import cherrypy
from cherrypy.lib.static import serve_file


current_dir = os.path.dirname(os.path.abspath(__file__))


def getImageFiles(root_dir):
        imageFiles = os.listdir(root_dir)
        imageFiles.sort()
        return imageFiles


def getModificationTime(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


class Root:
    @cherrypy.expose
    def index(self):
        return serve_file(os.path.join(current_dir,"motion_static/event_viewer.html"))


# API
class CameraStatus:
    def __init__(self, queue):
        self.queue = queue

    exposed = True
    def GET(self):
        if self.queue is not None:
            message = self.queue.get()
        else:
            message = "no connection"
        return json.dumps(message)



class FreeSpace:
    exposed = True
    def GET(self):
        s = os.statvfs('/')
        free_space = (s.f_bavail * s.f_frsize) / 1.0e9 # in gigabytes
        return json.dumps(free_space)




class EventFilenames:
    exposed = True
    def GET(self):
        image_files = getImageFiles("events")
        return json.dumps(image_files)



def run(queue=None, testing=True):
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.tree.mount(CameraStatus(queue),
                    '/api/camerastatus',
                    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})

    cherrypy.tree.mount(FreeSpace(),
                    '/api/freespace',
                    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})

    cherrypy.tree.mount(EventFilenames(),
                    '/api/eventfilenames',
                    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})


    cherrypy.config.update({'environment': 'production',
            'log.error_file': 'site.log',
            'log.screen': False})
    conf = {'/events': {'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.path.join(current_dir, 'events')},
            '/previews': {'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.path.join(current_dir, 'previews')},
            '/static': {'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.path.join(current_dir, 'motion_static')}}
    cherrypy.server.socket_host = '::'


    if testing == True:
        cherrypy.engine.autoreload.subscribe()
        cherrypy.config.update({'log.screen': True})

    cherrypy.quickstart(Root(), '/', config=conf)


if __name__ == '__main__':
    run(testing=True)
