#!/usr/bin/python
#
# Copyright 2012 SavingStar
    
import Image
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import socket,os,re
import json
from elaphe import barcode
from elaphe.upc import UpcA
import StringIO

class FrontPageHandler(tornado.web.RequestHandler):
    def get(self,upc=None):
        if upc == None:
            self.write("Please provide a barcode number")
        else:
            self.set_header("Content-Type", "image/png")
            upc = upc.encode('ascii','ignore')
            if len(upc) == 12:
                b = barcode('upca',upc,options=dict(includetext=True), scale=2, margin=1)
                fakefile = StringIO.StringIO()
                b.save(self,format='PNG')
            else:
                errorimg = Image.open('static/error.png')
                errorimg.save(self,format='PNG')
        #self.redirect('/static/error.png') 


def main():
    tornado.options.parse_command_line()
    # timeout in seconds
    timeout = 10
    socket.setdefaulttimeout(timeout)
    print("Starting Web Frontend for Waymoot")
    
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path" : "tornado-templates",
        "autoescape" : "xhtml_escape"
    }
    application = tornado.web.Application([
        (r"/" ,FrontPageHandler),
        (r"/(.*)" ,FrontPageHandler),
    ], **settings)
    
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
