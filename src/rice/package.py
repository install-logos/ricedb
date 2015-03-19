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
              raise error.corruption_error("Could not determine name of package.")

          if ("URL" in self.data):
              self.url = self.data["URL"]
          elif not old:
              raise error.corruption_error("Could not determine URL of package.")

          if ("Images" in self.data):
              self.images = self.data["Images"]

          if ("Program" in self.data):
              self.program = self.data["Program"]
          else:
              raise error.corruption_error("Could not determine the program of the package")

          if ("Files" in self.data):
              self.files = self.data["Files"]
          else:
              raise error.corruption_error("Could not determine the files of the package")

          if ("Path" in self.data):
              self.conf_root = self.data["Path"]
          else:
              raise error.corruption_error("Could not determine the installation location of the package")

          self.prog_path = util.RDBDIR + self.program
          self.path = util.RBBDIR + self.program + '/'+ self.name
          self.install_file = self.path + INSTALL

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
          switch_out()
          switch_in()

      def switch_out():
          os.chdir(self.prog_path)
          if(os.path.exists('./.active') and os.path.isfile('./.active')):
              #if rice is a rice_dB rice, read sysinfo.json to move non-vanilla files
              active_rice = open('./.active').readline().rstrip()
              if not os.path.exists('./' + active_rice):
                  raise error.corruption_error("The .active file referenced a nonexistant package")
              os.chdir('./' + active_rice)
              for k in self.Files.keys():
                  if not os.path.exists(self.conf_root + self.Files[k] + k):
                      raise error.corruption_error("Could not find the files specified in the rice")
                  os.rename(os.expanduser(self.conf_root + self.Files[k] + k), './' + k)
          # else:
          # TODO - Get switchout working for a local rice

      def switch_in():
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
