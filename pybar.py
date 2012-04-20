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
from barcode.writer import ImageWriter
import barcode
import ImageFont
from cStringIO import StringIO

class FrontPageHandler(tornado.web.RequestHandler):
    def get(self,upc=None):
        if upc == None:
            self.write("Please provide a barcode number")
        else:
            writer = ImageWriter()
            writer.set_options(options={'font_size':96})
            writer.font_size = 64
            upcimg = barcode.get_barcode('upc',upc,writer=writer)
            upcimg.save('static/' + upc)
            self.redirect('/static/' + upc + '.png')

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
