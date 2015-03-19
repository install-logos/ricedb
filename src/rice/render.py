# rice/render.py
#
# Defines the Render class.
#

import curses
import curses.textpad
import urllib.request
import os
from rice import query, w3m, util

SEARCHBAR_OFFSET = 2
SEARCHLEFT_OFFSET = 8

class Renderer(object):
  def __init__(self, w3mBinary='/usr/lib/w3m/w3mimgdisplay'):
    self.scr = curses.initscr()
    curses.noecho()       # don't echo characters
    curses.cbreak()       # no key buffering
    self.scr.keypad(True) # let curses handle keys
    self.scr.clear()
    self.results = None
    self.w3mEnabled = False
    if os.path.exists(w3mBinary):
      self.w3m = w3m.W3MImageDisplay(w3mBinary)
      self.w3mEnabled = True
  
    # Create a search box
    self.scr.addstr(0, 0, "Search:")
    self.textarea = curses.newwin(1, curses.COLS - 2, 0, SEARCHLEFT_OFFSET)
    self.text = curses.textpad.Textbox(self.textarea)
    self.text.stripspaces = True

    # Create result box delimiter
    for i in range(curses.COLS - 1):
      self.scr.insch(1, i, curses.ACS_HLINE)
    self.scr.refresh()

  def loop(self):
    while 1:
      try:
        self.textarea.erase()
        queryString = self.text.edit().strip()
        if queryString == "exit":
          self.end()
          break
        results = query.Query(queryString).getResults()
        self.populate(results)
      except Exception as e:
        print(str(e))


  # This will draw into a box defined by the passed in parameters
  def drawImage(self, tempFile, x, y, w, h):
    # Font dimensions
    fw, fh = util.getFontDimensions()
    # Image dimensions
    iw, ih = util.getImageDimensions(tempFile)
    # Box dimensions
    bw, bh = w * fw, h *fh
    
    # Scale the image to the box
    if iw > ih:
      scale = 1.0 * bw / iw
    else:
      scale = 1.0 * bh / ih
    iw = scale * iw
    ih = scale * ih

    # Get margin
    xM = (bw - iw) / 2
    yM = (bh - ih) / 2

    # Get x, y coordinates
    x = x * fw + xM
    y = y * fh + yM

    self.w3m.draw(tempFile, 1, x, y, w=iw, h=ih)

  def populate(self, results):
    if not self.results == None:
      del self.results
    self.results = curses.newpad(max(len(results), curses.LINES - 1), curses.COLS//2)
    self.results.clear()
    for i in range(curses.LINES - SEARCHBAR_OFFSET):
      self.results.insch(i, curses.COLS//2 - 2, curses.ACS_VLINE)
    i = 0
    for result in results:
      self.results.addstr(i, 0, result.name)
      if (not result.images == None) and (self.w3mEnabled):
        try:
          tempFile = util.RDBDIR + 'tmp'
          urllib.request.urlretrieve(result.images[0], tempFile)
          self.drawImage(tempFile, curses.COLS - curses.COLS/2, SEARCHBAR_OFFSET, curses.COLS/2, curses.LINES - SEARCHBAR_OFFSET)
        except Exception as e:
          # Who cares? it's just a picture.
          self.end()
          print(str(e))
          pass
      i += 1

    self.results.noutrefresh(0, 0, SEARCHBAR_OFFSET, 0, curses.LINES-1, curses.COLS-1)

  def end(self):
    self.scr.clear()
    curses.nocbreak()
    self.scr.keypad(False)
    curses.echo()
    curses.endwin()

