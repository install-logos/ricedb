#!/bin/env python
from rice import render

a = render.Renderer()
try:
  a.loop()
except Exception as e:
  a.end()
  print(str(e))

