# rice/query.py
#
# Defines the Query class.
#

import urllib.request
import json
from rice import error, util, package

class Query(object):
  def __init__(self, query):
    with open(util.RDBDIR + "config") as configFile:
      try:
        config = json.load(configFile)
      except Exception as e:
        raise error.CorruptionError("Invalid JSON: %s" %(e))
    try:
      request = urllib.request.Request(config["db"] + query)
      response = urllib.request.urlopen(request).read().decode('utf-8')
    except Exception as e:
      raise error.Error("Could not connect to server %s: %s" % (config["db"], e))
    try:
      self.results = json.loads(response)
    except Exception as e:
      raise error.CorruptionError("Could not read JSON from server: %s" %(e))

  def getResults(self):
    return [package.Package(i) for i in self.results]

