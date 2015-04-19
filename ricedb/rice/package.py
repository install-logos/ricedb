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

        if ("upstream" in self.data):
            self.upstream = self.data["upstream"]

        if ("program" in self.data):
            self.program = self.data["program"]
        else:
            raise error.CorruptionError("Could not determine the program of the package")

        if ("cover" in self.data):
            self.cover = self.data["cover"]

        if ("description" in self.data):
            self.description = self.data["description"]

        if ("author" in self.data):
            self.author = self.data["author"]

        if ("version" in self.data):
            self.version = self.data["version"]
        else:
            self.version = ""
