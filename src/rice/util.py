# rice/util.py
#
# Defines a various utility variables, functions and classes.
#

import os
import struct
import sys
import fcntl
import termios
import imghdr

RDBDIR = os.path.expanduser("~/.rdb/")

def get_image_dimensions(fname):
      # Determine the image type of fhandle and return its size.
      fhandle = open(fname, 'rb')
      head = fhandle.read(24)
      if len(head) != 24:
          return
      if imghdr.what(fname) == 'png':
          check = struct.unpack('>i', head[4:8])[0]
          if check != 0x0d0a1a0a:
              return
          width, height = struct.unpack('>ii', head[16:24])
      elif imghdr.what(fname) == 'gif':
          width, height = struct.unpack('<HH', head[6:10])
      elif imghdr.what(fname) == 'jpeg':
          try:
              fhandle.seek(0) # Read 0xff next
              size = 2
              ftype = 0
              while not 0xc0 <= ftype <= 0xcf:
                  fhandle.seek(size, 1)
                  byte = fhandle.read(1)
                  while ord(byte) == 0xff:
                      byte = fhandle.read(1)
                  ftype = ord(byte)
                  size = struct.unpack('>H', fhandle.read(2))[0] - 2
              # We are at a SOFn block
              fhandle.seek(1, 1)    # Skip `precision' byte.
              height, width = struct.unpack('>HH', fhandle.read(4))
          except Exception: #IGNORE:W0703
              return
      else:
          return
      return width, height

def get_font_dimensions():
      # Get the height and width of a character displayed in the terminal in
      # pixels.
      s = struct.pack("HHHH", 0, 0, 0, 0)
      fd_stdout = sys.stdout.fileno()
      x = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, s)
      rows, cols, xpixels, ypixels = struct.unpack("HHHH", x)
      if xpixels == 0 and ypixels == 0:
          binary_path = os.environ.get("W3MIMGDISPLAY_PATH", None)
          if not binary_path:
              binary_path = W3MIMGDISPLAY_PATH
          process = Popen([binary_path, "-test"],
              stdout=PIPE, universal_newlines=True)
          output, _ = process.communicate()
          output = output.split()
          xpixels, ypixels = int(output[0]), int(output[1])
          # adjust for misplacement
          xpixels += 2
          ypixels += 2
      return (xpixels // cols), (ypixels // rows)

def create():
    directory = ""
    file_list = {}
    print("Please specify the name of the rice")
    rice_name = input()
    while os.path.exists(self.prog_path + rice_name):
        print("Please use a rice name that is not already used")
        answer = input()
        if answer == "q":
            exit()
        else:
            rice_name = answer
    print("Please specify the root directory of your config files e.g. for i3 type in ~/.i3/")
    directory = os.expanduser(input())
    while not os.path.exists(directory):
        print("The specified directory does not exist. Try again or use q to quit")
        answer = input()
        if answer == "q":
            exit()
        else:
            directory = os.expanduser(answer)
    os.chdir(directory)
    for path, subdirs, files in os.walk("./"):
        for name in files:
            # This will use a ./, but this will be ok, though admittedly sketchy
            file_list[name] = path
    os.chdir(self.prog_path)
    os.mkdir(rice_name)
    os.chdir(rice_name)
    install_data = open("install.json")
    json.load(install_data)
    json_data.write(json.JSONEncoder().encode(file_list))
    json_data.write(json.JSONEncoder().encode({"Path":directory}))
    json_data.close()
