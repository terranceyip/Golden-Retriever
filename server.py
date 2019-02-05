from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import ssl
import os
import mimetypes
from cgi import parse_header, parse_multipart
from urlparse import parse_qs

class S(BaseHTTPRequestHandler):

    def _set_headers(self, mimetype='text/html'):
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()      

    def _set_headers_image(self, imgpath, type):
        statinfo = os.stat(imgpath)
        img_size = statinfo.st_size
        self.send_response(200)
        self.send_header("Content-type", "image/jpg")
        self.send_header("Content-length", img_size)
        self.end_headers()       

    def do_HEAD(self):
        self._set_headers()


    def send_webpage(self, sitefile):
        if (".png" in sitefile) or (".jpg" in sitefile) or (".gif" in sitefile) or (".bmp" in sitefile) or (".ico" in sitefile) :
            self._set_headers_image(sitefile, sitefile[-3:])
            image = open(sitefile,'rb')
            self.wfile.write(image.read())
            image.close()
            if sitefile == "item.png":
                image = open("item.png",'rb')
                newImage = open ("oldItem.png", 'wb')
                newImage.write(image.read())
                newImage.close()
                image.close()
                os.remove("item.png")
        else:
            site = open(sitefile, 'r')
            content = ""			
            mimetype, _ = mimetypes.guess_type(sitefile)
            self._set_headers(mimetype)
            for line in site.readlines():
                content += line
            site.close()
            self.wfile.write(content)


    def do_GET(self):
        sitefile = self.path[1:]
        if os.path.isfile(sitefile):
            self.send_webpage(sitefile)
        elif sitefile == "":
            self.send_webpage("index.html")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<html><body>bad url</body></html>")


    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars


    def do_POST(self):
        postvars = self.parse_POST()
        #print "keys: "
        #print postvars.keys()
        #print type(postvars["item"])
        #print len(postvars["item"])
        post_data = (postvars["item"])[0]
        location = open("item.png", 'w+b')
        location.write(post_data)
        location.close()
        self.send_response(200)
        self.send_webpage("accpeted.html")
        #for line in (postvars["file"]):
        #    location.write(line) # <-- Print post data
        #self._set_headers()
        #self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        '''
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        location = open("file.png", 'w')
        location.write(post_data) # <-- Print post data
        location.close()
        #token = file(self.ran_script_file, 'w')
        #token.close()
        #self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1><pre>" + post_data + "</pre></body></html>")
        print post_data
        '''




def run(server_class=HTTPServer, handler_class=S, port=80, use_ssl = False):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    if use_ssl:
        httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server.pem', server_side=True)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(use_ssl=bool(argv[1]))
    else:
        run()
