#!/usr/bin/python2.7
#
# Copyright 2012 SavingStar
    

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import socket,os,re
import json
from collections import OrderedDict
import barcode

class FrontPageHandler(tornado.web.RequestHandler):
    def get(self,upc=None):
        self.getvars()
        if upc == None:
            self.write("Please provide a barcode number")
        else:
            upc = barcode.get_barcode('upc', upc,writer=ImageWriter())
            filename = ean.save('barcodes/' + upc)


def main():
    tornado.options.parse_command_line()
    # timeout in seconds
    timeout = 10
    socket.setdefaulttimeout(timeout)
    print("Starting Web Frontend for Waymoot")
    
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "7cxqGjRMzxffffVxq2mnXalZbeUhaoDgnoTSvn0B",
        "login_url": "/login",
        "xsrf_cookies": True,
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
