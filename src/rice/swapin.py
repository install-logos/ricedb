import os
import json
import download
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

def swapin(program_name, rice_name, file_dict):
    """
    Takes a program name, rice name, and a dictionary of vanilla files/locations
    and will move files into locations specified by sysinfo.json and the file_dict
    argument
    """
    os.chdir('~/.riceDB/' + program_name + '/' + rice_name + '/')
    json_data = open("sysinfo.json")
    data = json.load(json_data)
    json_data.close()
    for file_name in data.keys():
        download.checkpath(data[file_name])
        os.rename('./' + file_name, data[file_name] + file_name)
    for file_name in file_dict.keys():
        download.checkpath(file_dict[file_name])
        os.rename('./' + file_name, file_dict[file_name] + file_name)
    os.chdir('~/.riceDB/' + program_name + '/')
    with open('.active', 'w') as fout:
        fout.write(rice_name)
    return (True, "")
