#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 seikichi
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Source from https://github.com/seikichi/pyw3mimg
#

from subprocess import Popen, PIPE

class W3MImage_display(object):
      """wrapper of w3mimgdisplay
      """

      def __init__(self, path='w3mimgdisplay', auto_sync=True):
          """
          Arguments:
          - `path`: path to w3mimgdisplay
          - `auto_sync`: do sync automaticaly
          """
          self._path = path
          self._auto_sync = auto_sync
          self._proc = Popen(self._path, shell=True, stdin=PIPE, stdout=PIPE)

      def write(self, s):
          self._proc.stdin.write(s.encode("utf-8"))
          self._proc.stdin.flush()

      def _draw(self, op, path, n, x, y, w=0, h=0, sx=0, sy=0, sw=0, sh=0):
          self.write('%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%s\n' % (op, n, x, y, w, h, sx, sy, sw, sh, path))
          if self._auto_sync:
              self.sync()

      def draw(self, path, n, x, y, w=0, h=0, sx=0, sy=0, sw=0, sh=0):
          """
          Arguments:
          - `n`: image index(?) n >= 1
          - `x`: 
          - `y`:
          - `w`:
          - `h`:
          - `sx`:
          - `sy`:
          - `sw`:
          - `sh`:
          - `path`: path of image file
          """
          self._draw(0, path, n, x, y, w, h, sx, sy, sw, sh)

      def redraw(self, path, n, x, y, w=0, h=0, sx=0, sy=0, sw=0, sh=0):
          """
          Arguments:
          - `n`: image index(?) n >= 1
          - `x`:
          - `y`:
          - `w`:
          - `h`:
          - `sx`:
          - `sy`:
          - `sw`:
          - `sh`:
          - `path`: path of image file
          """
          self._draw(1, path, n, x, y, w, h, sx, sy, sw, sh)

      def terminate(self):
          self.write('2;\n')

      def sync(self):
          self.write('3;\n')

      def nop(self):
          self.write('4;\n')
          self._proc.stdout.readline()

      def get_size(self, path):
          """
          get size of image
          Arguments:
          - `path`: path of image file
          """
          self.write('5;%s\n' % path)
          wh = self._proc.stdout.readline().split(' ')
          return (int(wh[0]), int(wh[1]))

      def clear(self, x, y, w, h):
          self.write('6;%d;%d;%d;%d\n', x, y, w, h)

