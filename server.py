from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random

hostName = "localhost"
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
  "Name": "test repo",
  "Description": "This is a sample of the description feild.",
  "URL": "http://localhost:8000/test.zip",
  "Images": ["http://localhost:8000/test.jpg"]
}
]"""]
    out += ["""[
{
  "Name": "test repo 1",
  "URL": "http://localhost/test.zip"
},
{
  "Name": "test repo 2",
  "URL": "http://localhost/test.zip"
},
{
  "Name": "test repo 3",
  "URL": "http://localhost/test.zip"
}
]"""]
    self.wfile.write(bytes(out[random.randint(0,1)], "utf-8"))

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
  myServer.serve_forever()
except KeyboardInterrupt:
  pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
