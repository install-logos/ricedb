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
  def __init__(self, data):
    self.data = data
    self.downloaded = False
    self.images = None
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

  def download(self):
    # Get the path of the download
    path = util.RDBDIR + self.name
    if not (os.path.exists(util.RDBDIR) and os.path.isdir(util.RDBDIR)):
      os.mkdir(util.RDBDIR)
    if (os.path.exists(path) and os.path.isdir(path)):
      raise error.Error("Path ("+path+") already exists.")
    # Download the file
    tempFile = path + TMPEXTENSION
    urllib.request.urlretrieve(self.url, tempFile)
    # Check if the file downloaded successfully
    if not (os.path.exists(tempFile) and zipfile.is_zipfile(tempFile)):
      raise error.CorruptionError("The download is corrupted. Please verify the integrity of your riceDB index file.")
    # Unzip the file
    z = zipfile.ZipFile(tempFile)
    for name in z.namelist():
      z.extract(name, path)
    os.remove(tempFile)
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
