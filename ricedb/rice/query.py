# rice/query.py
#
# Defines the Query class.
#
try:
    import urllib.request as request
except ImportError:
    import urllib2 as request
import json
import os
from . import error, util, package

class Query(object):
    def __init__(self, program_name, search_term, local=False):
        with open(util.RDBDIR + "config") as config_file:
            self.program_name = program_name
            try:
                config = json.load(config_file)
            except Exception as e:
                raise error.corruption_error("Invalid JSON: %s" %(e))
        if not local:
            try:
                # Will be modified to accept the query once testing is complete
                request = request.Request(config["db"] + "/query/?q=" + search_term)
                response = request.urlopen(request).read().decode('utf-8')
            except Exception as e:
                raise error.Error("Could not connect to server %s: %s" % (config["db"], e))
            try:
                self.results = json.loads(response)
            except Exception as e:
                raise error.corruption_error("Could not read JSON from server: %s" %(e))
        else:
            rices = json.load(open(os.path.expanduser(config["localdb"])))
            if search_term in rices[program_name]:
                self.results = [{"name":search_term,"program":program_name}]
            else:
                self.results = []
    def get_results(self):
        packs = []
        if self.results == []:
            return self.results
        if type(self.results) is dict:
            return [package.Package(self.results)]
        for i in self.results:
            # Temp fix, should be a server side thing eventually
            if i['program'] == self.program_name:
                packs.append(package.Package(i))
        return packs

