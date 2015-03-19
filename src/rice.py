#!/bin/env python
from rice import render

a = render.Renderer()
try:
      while 1:
          if a.loop():
              break
except Exception as e:
      a.end()
      print(str(e))

