from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random

hostname = "localhost"
hostPort = 9000

class MyServer(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    #self.path
    out = []
    out += ["""[
{
  "name": "test repo",
  "description": "This is a sample of the description field.",
  "url": "http://localhost:8000/test.zip",
  "images": ["http://localhost:8000/test.jpg"]
}
]"""]
    out += ["""[
{
  "name": "test repo 1",
  "url": "http://localhost/test.zip"
},
{
  "name": "test repo 2",
  "url": "http://localhost/test.zip"
},
{
  "name": "test repo 3",
  "url": "http://localhost/test.zip"
}
]"""]
    self.wfile.write(bytes(out[random.randint(0,1)], "utf-8"))

myServer = HTTPServer((hostname, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostname, hostPort))

try:
  myServer.serve_forever()
except KeyboardInterrupt:
  pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostname, hostPort))
