import os
import json
from . import download
import hashlib

def getHash(file_name, blocksize=2**20):
    sha = hashlib.sha256()
    with open(file_name, "rb") as fin:
        while True:
            buf = fin.read(blocksize)
            if not buf:
                break
            sha.update(buf)
    return sha.digest()

def setup(program_name, rice_name, file_dict):
    """
    Takes a program name, rice name, and a dictionary of vanilla files/locations
    and will move files into locations specified by sysinfo.json and the file_dict
    argument
    """
    os.chdir('~/.riceDB/' + program_name + '/' + rice_name + '/')
    json_data = open("sysinfo.json")
    sha_checksums = open("checksums.sha")
    data = json.load(json_data)
    checksums = json.load(sha_checksums)
    json_data.close()
    sha_checksums.close()
    for file_name in data.keys():
        if getHash(file_name) is checksums[file_name]:
            download.checkpath(data[file_name])
            os.rename('./' + file_name, data[file_name] + file_name)
        else:
            return (False, "WARNING, file checksums did not match expected values. Please ensure your connection is secure and that you have an up-to-date index file")
    for file_name in file_dict.keys():
        if getHash(file_name) is checksums[file_name]:
            download.checkpath(file_dict[file_name])
            os.rename('./' + file_name, file_dict[file_name] + file_name)
        else:
            return (False, "WARNING, file checksums did not match expected values. Please ensure your connection is secure and that you have an up-to-date index file")
    os.chdir('~/.riceDB/' + program_name + '/')
    with open('.active', 'w') as fout:
        fout.write(rice_name)
    return (True, "")
