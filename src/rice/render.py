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
      self.scr.addch(1, i, curses.ACS_HLINE)
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

  def populate(self, results):
    self.end()
    if not self.results == None:
      del self.results
    self.results = curses.newpad(max(len(results), curses.LINES - 1), curses.COLS - 1)
    self.results.erase()
    i = 0
    for result in results:
      self.results.addstr(i, 0, result.name)
      if not result.images == None:
        tempFile = util.RDBDIR + 'tmp'
        try:
          urllib.request.urlretrieve(result.images[0], tempFile)
        except Exception as e:
          print(str(e))
        self.w3m.draw(tempFile, 1, 100, 20, w=100, h=100)
      i += 1

    self.results.noutrefresh(0, 0, SEARCHBAR_OFFSET, 0, curses.LINES-1, curses.COLS-1)

  def end(self):
    self.scr.clear()
    curses.nocbreak()
    self.scr.keypad(False)
    curses.echo()
    curses.endwin()

