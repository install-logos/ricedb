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
        self.program_name = program_name
        config = self.get_config_data()
        if not local:
            try:
                # Will be modified to accept the query once testing is complete
                server_request = request.Request(config["db"] + "/query/?q=" + search_term)
                response = request.urlopen(server_request).read().decode('utf-8')
            except Exception as e:
                raise error.Error("Could not connect to server %s: %s" % (config["db"], e))
            try:
                self.results = json.loads(response)
            except Exception as e:
                raise error.corruption_error("Could not read JSON from server: %s" %(e))
        else:
            rices = json.load(open(os.path.expanduser(config["localdb"])))
            self.results = []
            if search_term in rices.get(program_name, {}):
                self.results.append({"name": search_term, "program": program_name})

    @staticmethod
    def get_config_data():
        with open(util.RDBDIR + "config") as config_file:
            try:
                return json.load(config_file)
            except Exception as e:
                raise error.corruption_error("Invalid JSON: %s" % e)

    def get_results(self):
        """
        Formats the query results from Query()
        as package objects

        Returns:
            list of Package objects
        """
        packs = []
        for i in self.results:
            # Temp fix, should be a server side thing eventually
            if i.get('program') == self.program_name:
                packs.append(package.Package(i))
        return packs

