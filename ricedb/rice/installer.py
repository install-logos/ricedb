# rice/package.py
#
# Defines the Package class.
#

import json
import os
import urllib.request
import zipfile
from . import error, util, render

TMPEXTENSION = "-tmp.zip"
INSTALL = "install.json"

class Installer(object):
    """
    Handles downloading and installing rices for a specific package
    Deals with all functionality concerning configurations/packages
    """
    def __init__(self, prog_name, rice_name, url=""):
        self.local = False
        self.name = rice_name
        self.program = prog_name
        self.url = url
        self.prog_path = util.RDBDIR + self.program + '/'
        self.path = self.prog_path + self.name + '/'
        if url == "":
            self.check_files()

    def check_files(self): 
        self.local = True
        self.install_file = self.path + INSTALL
        if not (os.path.exists(self.install_file) and os.path.isfile(self.install_file)):
            raise error.corruption_error("Package has no install file.")
        with open(self.install_file) as f:
            try:
                self.install_data = json.load(f)
            except Exception as e:
                raise error.corruption_error("Could not read JSON: %s" %(e))
            if "files" in self.install_data:
                self.files = self.install_data['files']
            else:
                raise error.corruption_error("Could not read the files in the JSON")
            if "conf_root" in self.install_data:
                self.conf_root = os.path.expanduser(self.install_data["conf_root"])
            else:
                raise error.corruption_error("Could not read the config root in the JSON")

    def validate_extraction(self):
        os.chdir(self.path)
        path_files = os.listdir('.')
        # Remove files from sub folder
        if len(path_files) == 1 and os.path.isdir(path_files[0]):
            os.chdir(path_files[0])
            for f in os.listdir('.'):
                os.rename('./'+f,'../'+f)
        os.chdir('../')
        os.rmdir(path_files[0])

    def download(self):
        # Get the path of the download
        if self.local:
            raise error.unentered_data_error("This is a local rice, it cannot be downloaded")
        if not (os.path.exists(util.RDBDIR) and os.path.isdir(util.RDBDIR)):
            os.makedirs(util.RDBDIR)
        if not (os.path.exists(self.prog_path)):
            os.makedirs(self.prog_path)
        if (os.path.exists(self.path) and os.path.isdir(self.path)):
            raise error.Error("Path ("+self.path+") already exists.")
        # Download the file
        temp_file = self.prog_path + TMPEXTENSION
        urllib.request.urlretrieve(self.url, temp_file)
        # Check if the file downloaded successfully
        if not (os.path.exists(temp_file) or not zipfile.is_zipfile(temp_file)):
            raise error.corruption_error("The download is corrupted. Please verify the integrity of your rice_dB index file.")
        # Unzip the file
        z = zipfile.ZipFile(temp_file)
        for name in z.namelist():
            z.extract(name, self.path)
        self.validate_extraction()
        os.remove(temp_file)
        self.check_files()

    def install(self,force=False):
        # Force install, ignoring current files installed
        if not force:
            self.switch_out()
        self.switch_in()

    # Checks if the currently installed rice is defined in riceDB, returns True if it is, False if not
    def check_install(self):
        os.chdir(self.prog_path)
        # If there isn't an active riceDB rice, create a new local rice
        return (os.path.exists('./.active') and os.path.isfile('./.active'))
        
    def switch_out(self):
        os.chdir(self.prog_path)
        # If there isn't an active riceDB rice, create a new local rice
        current_name = open('./.active').readline().rstrip()
        os.chdir(self.prog_path + current_name)
        old_install_file = self.prog_path + current_name + '/' + INSTALL
        if not (os.path.exists(old_install_file) and os.path.isfile(old_install_file)):
            raise error.corruption_error("Package has no install file.")
        with open(old_install_file) as f:
            try:
                old_install_data = json.load(f)
            except Exception as e:
                raise error.corruption_error("Could not read JSON: %s" %(e))
            if "files" in old_install_data:
                old_files = old_install_data['files']
            else:
                raise error.corruption_error("Could not read the files in the JSON")
            if "conf_root" in old_install_data:
                old_conf_root = os.path.expanduser(old_install_data["conf_root"])
            else:
                raise error.corruption_error("Could not read the config root in the JSON")
        for k in old_files.keys():
            if not os.path.exists(old_conf_root + old_files[k] + k):
                raise error.corruption_error("Could not find the files specified in the rice")
            os.remove(old_conf_root + old_files[k] + k)

    def switch_in(self):
        os.chdir(self.path)
        if not (os.path.exists(self.conf_root)):
            os.makedirs(self.conf_root)
        for k in self.files.keys():
            if not (os.path.exists('./' + k)):
                os.chdir(self.prog_path)
                # switch_in(open('./.active').readline().rstrip())
                # We need to undo the switch out here
                raise error.corruption_error("Nonexistant files referenced in install.json")
            self.validate_dir(self.files[k])
            os.symlink(os.path.abspath(k), self.conf_root + self.files[k] + k)
        os.chdir(self.prog_path)
        with open('./.active','w') as fout:
            fout.write(self.name)

    # Makes folders in config_root if necessary
    def validate_dir(self,full_path):
        if full_path == "./":
            return
        os.chdir(self.conf_root)
        os.makedirs(full_path)
