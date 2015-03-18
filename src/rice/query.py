# rice/query.py
#
# Defines the Query class.
#

import urllib
import json
from rice import error, util

class Query(object):
  def __init__(self, query):
    with open(util.RDBDIR + "config") as configFile:
      try:
        config = json.loads(configFile)
      except Exception as e:
        raise error.CorruptionError("Invalid json: %s" %(e))
    try:
      response = urllib2.open(config["db"] + query)
    except Exception as e:
      raise error.Error("Could not connect to server %s" % (config["db"]))
    try:
      self.results = json.loads(response)
    except Exception as e:
      raise error.CorruptionError("Could not read JSON from server: %s" %(e))

  def getResults(self):
    return [Package(i) for i in self.results]

