import os
import urllib
import zipfile
riceDB_path = os.environ['HOME'] + "/.riceDB"
print(riceDB_path)
def checkpath(path):
    if (os.path.exists(path) and os.path.isdir(path)):
        os.chdir(path)
    else:
        os.mkdir(path)
        os.chdir(path)
def download(gitlink, progname, ricename):
    checkpath(riceDB_path)
    checkpath("./" + progname + "-rice")
    if (os.path.exists("./" + ricename) and os.path.isdir(ricename)):
        return (False;"Rice already exists")
    else:
        urllib.urlretrieve(gitlink, ricename + "-tmp.zip")
        if(os.path.exists(ricename + "-tmp.zip") and  zipfile.is_zipfile(ricename +"-tmp.zip")):
            z = zipfile.ZipFile(ricename + "-tmp.zip")
            for name in z.namelist():
                output="./"
                z.extract(name,output)
            os.rename(ricename + "-master",ricename)
