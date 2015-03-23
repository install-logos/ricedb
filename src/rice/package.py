# rice/package.py
#
# Defines the Package class.
#

import json
import os
import urllib.request
import zipfile
from rice import error, util

TMPEXTENSION = "-tmp.zip"
INSTALL = "install.json"

class Package(object):
    """
    Handles downloading and installing rices for a specific package
    Deals with all functionality concerning configurations/packages
    """
    def __init__(self, prog_name, rice_name, url=""):
        self.name = rice_name
        self.program = prog_name
        self.url = url
        self.prog_path = util.RDBDIR + self.program + '/'
        self.path = self.prog_path + self.name + '/'
        self.install_file = self.path + INSTALL
        if not (os.path.exists(install_file) and os.path.isfile(install_file)):
            raise error.corruption_error("Package has no install file.")
        with open(self.install_file) as f:
            try:
                self.install_data = json.load(f)
            except Exception as e:
                raise error.corruption_error("Could not read JSON: %s" %(e))
            ## Now execute the installation
            if "files" in self.install_data:
                self.files = self.install_data['files']
            else:
                raise error.corruption_error("Could not read the files in the JSON")
            if "conf_root" in self.install_data:
                self.conf_root = self.install_data["conf_root"]
            else:
                raise error.corruption_error("Could not read the config root in the JSON")
    
    def download(self):
        # Get the path of the download
        if self.url == "":
            raise error.unentered_data_error("The URL field was not specified, this is a local rice")
        if not (os.path.exists(util.RDBDIR) and os.path.isdir(util.RDBDIR)):
            os.mkdir(util.RDBDIR)
        if not (os.path.exists(prog_path)):
            os.mkdir(prog_path)
        if (os.path.exists(path) and os.path.isdir(path)):
            raise error.Error("Path ("+path+") already exists.")
        # Download the file
        temp_file = self.prog_path + TMPEXTENSION
        urllib.request.urlretrieve(self.url, temp_file)
        # Check if the file downloaded successfully
        if not (os.path.exists(temp_file) and zipfile.is_zipfile(temp_file)):
            raise error.corruption_error("The download is corrupted. Please verify the integrity of your rice_dB index file.")
        # Unzip the file
        z = zipfile.zip_file(temp_file)
        for name in z.namelist():
            z.extract(name, path)
        os.remove(temp_file)
        with open(self.install_file, 'w') as fout:
            json.dump(self.data, fout)

    def install(self):
        os.chdir(self.prog_path)
        if (os.path.exists('./.active') and os.path.isfile('./.active')):
            current_rice = Package(self.program, open('./active').readline().rstrip())
        else:
            current_name = util.create_rice()
            current_rice = Package(self.program,current_name) 
        current_rice.switch_out()
        self.switch_in()

    def switch_out(self):
        os.chdir(self._path)
        for k in self.files.keys():
            if not os.path.exists(self.conf_root + self.files[k] + k):
                raise error.corruption_error("Could not find the files specified in the rice")
            os.rename(os.expanduser(self.conf_root + self.files[k] + k), './' + k)

    def switch_in(self):
        os.chdir(self.path)
        if not (os.path.exists(self.conf_root)):
            os.mkdir(self.conf_root)
        for k in self.files.keys():
            if not (os.path.exists('./' + k)):
                os.chdir(self.prog_path)
                switch_in(open('./.active').readline().rstrip())
                raise error.corruption_error("Nonexistant files referenced in install.json")
                os.rename('./' + k, os.expanduser(self.conf_root) + self.files[k] + k)
        os.chdir(self.prog_path)
        with open('./.active','w') as fout:
            fout.write(self.name)
        return self
