#!/usr/bin/python

from multiprocessing import Manager
from threading import Thread
from time import sleep
import json
import os
import hashlib
from datetime import datetime
import random

from Ping import ping
from Resident import resident

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

#----------------------------------------------------------------------------------------------------------
class MainHandler(tornado.web.RequestHandler):
    def get(self):
      self.render("templates/index.html")

class PingHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous    
    def post(self):
        self.user_hash = self.request.arguments['hash'][0]
        self.scheduler = tornado.ioloop.PeriodicCallback(self._check, 1000)
        self.scheduler.start()

    def _check(self):
        md5 = PingHandler.equalHash(self.user_hash)
        if md5:
            self.scheduler.stop()
            if Global.result:
                print Global.result
                if not Global.pingtime: Global.pingtime = -1
                json_res = json.dumps([Global.pingtime, md5, Global.result])
                self.set_header("Content-Type", "application/json")
                self.write(json_res)
            else:
                self.write('Data not avaliable yet...')
            self.finish()


    @staticmethod
    def equalHash(user_hash):        
        md5 = hashlib.md5()
        md5.update(str(Global.result))

        if (user_hash == md5.hexdigest()):
            return None
        else:
            return md5.hexdigest()

           
#----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    pingList = ['192.168.13.44', '172.22.22.1', '172.22.22.189', 'google.com', 'localhost', '192.168.10.14']
    #pingList = ['google.com', 'ya.ru']

    manager = Manager()
    Global = manager.Namespace()
    Global.result = {}
    Global.pingtime = 0

    Global.result = [{'192.168.1.2': 0}, {'192.168.1.3': 2}, {'google.com': 2}]

    # Start inifinite thread in background
    infinite = Thread(target=resident, args=(ping, Global, pingList))
    infinite.setDaemon(True)
    infinite.start()
    
    define("port", default=8888, help="run on the given port", type=int)

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }

    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/ping", PingHandler),        
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    
    print "the end of the world..."
    

 
