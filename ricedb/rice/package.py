from . import error


class Package(object):
    """
    Collect the data related to a package 
    upon instantiation
    """

    def __init__(self, data):
        self.data = data
        self.images = None

        try:
            self.name = self.data["name"]
        except KeyError:
            raise error.CorruptionError("Could not determine name of package.")

        try:
            self.program = self.data.get("program")
        except:
            raise error.CorruptionError("Could not determine program name.")

        self.upstream = self.data.get("upstream")
        self.cover = self.data.get("cover", "")
        self.description = self.data.get("description", "")
        self.author = self.data.get("author", "")
        self.version = self.data.get("version", "")
