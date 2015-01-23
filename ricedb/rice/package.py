from . import error
import json
class Package(object):
  def __init__(self, data):
    self.data = data
    self.images = None
    if ("name" in self.data):
      self.name = self.data["name"]
    else:
      raise error.CorruptionError("Could not determine name of package.")

    if ("url" in self.data):
      self.url = self.data["url"]

    if ("program" in self.data):
        self.program = self.data["program"]
    else:
        raise error.CorruptionError("Could not determine the program of the package")

    if ("images" in self.data):
      self.images = self.data["images"]

