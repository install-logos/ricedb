# rice/render.py
#
# Defines the Render class.
#

import curses
import curses.textpad
from rice import query

class Renderer(object):
  def __init__(self):
    self.scr = curses.initscr()
    curses.noecho()       # don't echo characters
    curses.cbreak()       # no key buffering
    self.scr.keypad(True) # let curses handle keys
    self.scr.clear()
  
    # Create a search box
    self.scr.addstr(0, 0, "Search:")
    self.textarea = curses.newwin(1, curses.COLS - 2, 0, 8)
    self.text = curses.textpad.Textbox(self.textarea)
    self.text.stripspaces = True

    # Create result box delimiter
    for i in range(curses.COLS - 1):
      self.scr.addch(1, i, curses.ACS_HLINE)

    self.scr.refresh()

  def loop(self):
    while 1:
      self.textarea.clear()
      queryString = self.text.edit().strip()
      if queryString == "exit":
        self.end()
        break
      results = query.Query(queryString).getResults()
      self.populate(results)

  def populate(self, results):
    self.end()
    self.results = curses.newwin(curses.LINES - 2, curses.COLS - 1, 1, 1)
    self.scr.addstr(0, 0, "Search:")
    for i in range(curses.COLS - 1):
      self.scr.addch(1, i, curses.ACS_HLINE)
    i = 2
    for result in results:
      self.scr.addstr(i, 0, result.name)
    self.scr.refresh()
    self.textarea.refresh()

  def end(self):
    self.scr.clear()
    curses.nocbreak()
    self.scr.keypad(False)
    curses.echo()
    curses.endwin()

