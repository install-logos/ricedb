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
    def __init__(self, data, old=""):
        self.data = data
        #print("Initialized with data + " + self.data)
        self.downloaded = False
        if not old == "":
            self.downloaded = True
        self.images = None
        self.program = None
        self.files = None
        self.conf_root = None
        required_fields = ["name", "url", "program"]
        optional_fields = ["images", "description"]
        for key in required_fields:
            value = self.data.get(key)
            if not value:
                raise error.corruption_error('Could not determine {} of package'.format(key))
            setattr(self, key.lower(),value)
        for key in optional_fields:
            value = self.data.get(key)
            if value:
                setattr(self, key.lower(),value)
        self.prog_path = util.RDBDIR + self.program + '/'
        self.path = self.prog_path + self.name + '/'
        self.install_file = self.path + INSTALL
        print("Initialized rice " + self.name)
    def download(self):
        # Get the path of the download
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
        self.downloaded = True

    def install(self):
        if not self.downloaded:
            raise error.Error("Package is not downloaded.")
        install_file = path + INSTALL
        if not (os.path.exists(install_file) and os.path.isfile(install_file)):
            raise error.corruption_error("Package has no install file.")
        with open(install_file) as f:
            try:
                self.install_data = json.load(f)
            except Exception as e:
                raise error.corruption_error("Could not read JSON: %s" %(e))
            ## Now execute the installation
            if "Files" in self.install_data:
                file_locs = self.install_data['Files']
            else:
                raise error.corruption_error("Could not read the files in the JSON")
        self.switch_out()
        self.switch_in()

    def switch_out(self):
        os.chdir(self.prog_path)
        if(os.path.exists('./.active') and os.path.isfile('./.active')):
            #if rice is a rice_dB rice, read sysinfo.json to move non-vanilla files
            active_rice = open('./.active').readline().rstrip()
            if not os.path.exists('./' + active_rice):
                raise error.corruption_error("The .active file referenced a nonexistant package")
            os.chdir('./' + acive_rice)
            for k in self.Files.keys():
                if not os.path.exists(self.conf_root + self.Files[k] + k):
                    raise error.corruption_error("Could not find the files specified in the rice")
                os.rename(os.expanduser(self.conf_root + self.Files[k] + k), './' + k)
        # TODO - Get switchout working for a local rice
        else:
            directory = ""
            file_list = {}
            print("Please specify the name of the rice")
            rice_name = input()
            while os.path.exists(self.prog_path + rice_name):
                print("Please use a rice name that is not already used")
                answer = input()
                if answer == "q":
                    exit()
                else:
                    rice_name = answer
            print("Please specify the root directory of your config files e.g. for i3 type in ~/.i3/")
            directory = os.expanduser(input())
            while not os.path.exists(directory):
                print("The specified directory does not exist. Try again or use q to quit")
                answer = input()
                if answer == "q":
                    exit()
                else:
                    directory = os.expanduser(answer)
            os.chdir(directory)
            for path, subdirs, files in os.walk("./"):
                for name in files:
                    # This will use a ./, but this will be ok, though admittedly sketchy
                    file_list[name] = path
            os.chdir(self.prog_path)
            os.mkdir(rice_name)
            os.chdir(rice_name)
            install_data = open("install.json")
            json.load(install_data)
            json_data.write(json.JSONEncoder().encode(file_list))
            json_data.write(json.JSONEncoder().encode({"Path":directory}))
            json_data.close()
    def switch_in(self):
        os.chdir(self.path)
        if not (os.path.exists(self.conf_root)):
            os.mkdir(self.conf_root)
        for k in self.Files.keys():
            if not (os.path.exists('./' + k)):
                os.chdir(self.prog_path)
                switch_in(open('./.active').readline().rstrip())
                raise error.corruption_error("Nonexistant files referenced in install.json")
                os.rename('./' + k, os.expanduser(self.conf_root) + self.Files[k] + k)
        os.chdir(self.prog_path)
        with open('./.active','w') as fout:
            fout.write(self.name)
