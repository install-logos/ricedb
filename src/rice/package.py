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
    self.confRoot = None
    if ("Name" in self.data):
      self.name = self.data["Name"]
    else:
      raise error.CorruptionError("Could not determine name of package.")

    if ("URL" in self.data):
      self.url = self.data["URL"]
    elif not old:
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
        self.confRoot = self.data["Path"]
    else:
      raise error.CorruptionError("Could not determine the installation location of the package")

    self.progPath = util.RBDIR + self.program
    self.path = util.RDBDIR + self.program + '/'+ self.name
    self.installFile = self.path + INSTALL

  def download(self):
    # Get the path of the download
    if not (os.path.exists(util.RDBDIR) and os.path.isdir(util.RDBDIR)):
      os.mkdir(util.RDBDIR)
    if not (os.path.exists(progPath)):
        os.mkdir(progPath)
    if (os.path.exists(path) and os.path.isdir(path)):
      raise error.Error("Path ("+path+") already exists.")
    # Download the file
    tempFile = self.progPath + TMPEXTENSION
    urllib.request.urlretrieve(self.url, tempFile)
    # Check if the file downloaded successfully
    if not (os.path.exists(tempFile) and zipfile.is_zipfile(tempFile)):
      raise error.CorruptionError("The download is corrupted. Please verify the integrity of your riceDB index file.")
    # Unzip the file
    z = zipfile.ZipFile(tempFile)
    for name in z.namelist():
      z.extract(name, self.path)
    os.remove(tempFile)
    with open(self.installFile, 'w') as fout:
        json.dump(self.data, fout)
    self.downloaded = True

  def install(self):
    if not self.downloaded:
      raise error.Error("Package is not downloaded.")
    installFile = path + INSTALL
    if not (os.path.exists(installFile) and os.path.isfile(installFile)):
      raise error.CorruptionError("Package has no install file.")
    with open(installFile) as f:
      try:
        self.installData = json.load(f)
      except Exception as e:
        raise error.CorruptionError("Could not read JSON: %s" %(e))
    ## Now execute the installation
    if "Files" in self.installData:
        fileLocs = self.installData['Files']
    else raise error.CorruptionError("Could not read the files in the JSON")
    switchOut() 
    switchIn()

  def switchOut():
    os.chdir(self.progPath)
    if(os.path.exists('./.active') and os.path.isfile('./.active')):
        #if rice is a riceDB rice, read sysinfo.json to move non-vanilla files
        activeRice = open('./.active').readline().rstrip()
        if not os.path.exists('./' + activeRice):
            raise error.CorruptionError("The .active file referenced a nonexistant package")
        os.chdir('./' + activeRice)
        for k in self.Files.keys():
            os.rename(os.expanduser(self.confRoot + self.Files[k] + k), './' + k)
        return activeRice
    else:
        # TODO - Get switchout working for a local rice

  def switchIn():
    os.chdir(self.path)
    if not (os.path.exists(self.confRoot)):
        os.mkdir(self.confRoot)
    for k in self.Files.keys():
        if not (os.path.exists('./' + k)):
            os.chdir(self.progPath)
            switchIn(open('./.active').readline().rstrip())
            raise error.CorruptionError("Nonexistant files referenced in install.json")    
        os.rename('./' + k, os.expanduser(self.confRoot) + self.Files[k] + k)
    os.chdir(self.progPath)
    with open('./.active','w') as fout:
        fout.write(self.name)

