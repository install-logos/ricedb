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
  def __init__(self, data, old=False):
    self.data = data
    self.downloaded = False
    if old:
        self.downloaded = True
    self.images = None
    self.program = None
    self.files = None
    self.conf_root = None
    if ("Name" in self.data):
      self.name = self.data["Name"]
    else:
      raise error.CorruptionError("Could not determine name of package.")

    if ("URL" in self.data):
      self.url = self.data["URL"]
    else:
      raise error.CorruptionError("Could not determine URL of package.")

    if ("Images" in self.data):
      self.images = self.data["Images"]
    
    if ("Program" in self.data):
        self.program = self.data["Program"]
    else:
        raise error.CorruptionError("Could not determine the program of the package")
    
    if ("Files" in self.data):
        self.files = self.data["Files"]
    else:
        raise error.CorruptionError("Could not determine the files of the package")
  
    if ("Path" in self.data):
        self.conf_root = self.data["Path"]
    else:
      raise error.CorruptionError("Could not determine the installation location of the package")
  def download(self):
    # Get the path of the download
    self.prog_path = util.RBDIR + self.program
    self.path = util.RDBDIR + self.program + '/'+ self.name
    self.install_file = self.path + INSTALL

    if not (os.path.exists(util.RDBDIR) and os.path.isdir(util.RDBDIR)):
      os.mkdir(util.RDBDIR)
    if not (os.path.exists(prog_path)):
        os.mkdir(prog_path)
    if (os.path.exists(path) and os.path.isdir(path)):
      raise error.Error("Path ("+path+") already exists.")
    # Download the file
    tempFile = self.prog_path + TMPEXTENSION
    urllib.request.urlretrieve(self.url, tempFile)
    # Check if the file downloaded successfully
    if not (os.path.exists(tempFile) and zipfile.is_zipfile(tempFile)):
      raise error.CorruptionError("The download is corrupted. Please verify the integrity of your riceDB index file.")
    # Unzip the file
    z = zipfile.ZipFile(tempFile)
    for name in z.namelist():
      z.extract(name, path)
    os.remove(tempFile)
    with open(self.install_file, 'w') as fout:
        json.dump(self.data, fout)
    self.downloaded = True

  def install(self):
    if not self.downloaded:
      raise error.Error("Package is not downloaded.")
    install_file = path + INSTALL
    if not (os.path.exists(install_file) and os.path.isfile(install_file)):
      raise error.CorruptionError("Package has no install file.")
    with open(install_file) as f:
      try:
        self.install_data = json.load(f)
      except Exception as e:
        raise error.CorruptionError("Could not read JSON: %s" %(e))
    ## Now execute the installation
    if "Files" in self.install_data:
        file_locs = self.install_data['Files']
    else raise error.CorruptionError("Could not read the files in the JSON")
    switch_out(self.prog_name) 

  def switch_out(prog_name):
    os.chdir(self.prog_path)
    if(os.path.exists('./.active') and os.path.isfile('./.active')):
        #if rice is a riceDB rice, read sysinfo.json to move non-vanilla files
        active_rice = open('./.active').readline().rstrip()
        if not os.path.exists('./' + active_rice):
            raise error.CorruptionError("the .active file referenced a nonexistant package")
        os.chdir('./' + active_rice)
        for k in self.Files.keys():
            os.rename(os.expanduser(self.conf_root + self.Files[k] + k), './' + k)
        return (active_rice, True, "")
    else:
        # TODO - Get switchout working for a local rice
        #else ask user for non-vanilla files
        user_files = {}
        another = 'y'
        rice_name = ""
        while another == 'y':
            print("Please enter the path of your non-vanilla files:\n (type n to continue)")
            user_inp = input()
            if os.path.isfile(user_inp):
                t = os.path.split(user_inp)
                user_files[t[1]]=(t[0] + '/')
                print("Do you have another non-vanilla file beside the ones you already typed in ? (y/n)")
                another = input().lower()
            elif user_inp is 'n':
                break 
            elif user_inp is '':
                break 
            else:
                print("Filepath " + user_inp + " is not valid, please retry.")
        print("Please choose a name for your personnal rice:")
        rice_name = input()
        while os.path.exists('~/.riceDB/' + prog_name + '/' + rice_name):
            print("A rice with this name already exists, please choose another name:")
            rice_name = input()
        os.mkdir(rice_name)
        # os.chdir('./' + rice_name + '/')
        swfiles(user_files,rice_name)
        swfiles(dict_file,'./')
        if len(user_files) > 0:
            serialize(user_file,'sysinfo.json')
        else:
            with open('sysinfo.json','w') as fout:
                fout.write("{\n}")
        return (rice_name,True,"")
