import os
import urllib.request
import zipfile

riceDB_path = os.environ['HOME'] + "/.riceDB"
# print(riceDB_path)

def check(path):
    path = path.replace("~/",os.environ["HOME"] + "/")

    if not (os.path.exists(path) and os.path.isdir(path)):
        os.mkdir(path)
    return path

def checkpath(path):
    path = path.replace("~/",os.environ["HOME"] + "/")
    if (os.path.exists(path) and os.path.isdir(path)):
        os.chdir(path)
    else:
        os.mkdir(path)
        os.chdir(path)

def download(gitlink, progname, ricename):
    checkpath(riceDB_path)
    checkpath("./" + progname + '/')
    if (os.path.exists("./" + ricename) and os.path.isdir(ricename)):
        return (False,"This rice already exists")
    else:
        urllib.request.urlretrieve(gitlink, ricename + "-tmp.zip")
        if(os.path.exists(ricename + "-tmp.zip") and zipfile.is_zipfile(ricename +"-tmp.zip")):
            z = zipfile.ZipFile(ricename + "-tmp.zip")
            for name in z.namelist():
                output="./"
                z.extract(name,output)
            os.rename(ricename + "-master",ricename)
            os.remove(ricename+"-tmp.zip")
            return (True,"")
        else:
            return (False,"The download is corrupted. Please verify the integrity of your riceDB index file")
