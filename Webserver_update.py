from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.request import urlopen
from urllib.error import URLError,HTTPError
from urllib.parse import urlparse
import time
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #lets use url parse
        parsed = urlparse(self.path)
        #scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment=''

    #    print(self.request_version)
    #    print(parsed.path)
        if self.request_version=='HTTP/1.0':
            print("wrong requrest version")
            self.send_response(400, 'Bad Request')
 #           self.send_header('Content-type','text/html')
        elif parsed.path=='/mir.html':
            print("error!!!!!")
            self.send_error(404,'Not Found')
#            self.send_header('Content-type','')
        else:
            if parsed.path=='/test/image.jpg':
                self.send_response(200,'OK')
                self.send_header('Content-type','IMAGE/JPEG')
                self.end_headers()
                print('image')
                print(parsed.path)
           
           

        self.end_headers()
    #    if self
     #       self.send_header('Content-type','IMAGE/JPEG')


if __name__=='__main__':
    MyServer=HTTPServer(('',8888),MyHandler)
    print('Started WebServer on port 8888')
    print("Press Ctrl + c to quit WebServer")
    MyServer.serve_forever()