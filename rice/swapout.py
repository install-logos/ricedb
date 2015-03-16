import os
import json

def switch(progname, dictfile):
    os.chdir('~/.riceDB/' + progname)
    if(os.path.exists('./.active') and os.path.isfile('./.active')):
        active_rice = open('./.active').readline().rstrip()
        os.chdir('./' + active_rice)
        json_data = open('sysinfo.json')
        data = json.load(json_data)
        json_data.close()
        key = list(data.keys())
        for k in key:
            os.rename(data[k] + k, './' + k)
        key = list(dictfile.keys())
        for k in key:
            os.rename(dictfile[k] + k, './' + k)
    else:

