from rice import download
import os
import json
#TODO add hashing
def serialize(dictionary, json_file):
    #encodes a dict into a json file
    json_data = open(json_file)
    json.load(json_data)
    json_data.write(json.JSONEncoder().encode(dictionary))
    json_data.close()

def swfiles(dictionary, folder):
    #moves files specified in dictionary into folder and changes working dir to that folder
    os.chdir(folder)
    key = list(dictionary.keys())
    for k in key:
        loc = dictionary[k].replace("~","")
        os.rename(os.environ['HOME'] + loc + k, './' + k)

def switch(prog_name, dict_file):
    download.checkpath(os.environ['HOME'] + '/.riceDB/' + prog_name + '/')
    if(os.path.exists('./.active') and os.path.isfile('./.active')):
        #if rice is a riceDB rice, read sysinfo.json to move non-vanilla files
        active_rice = open('./.active').readline().rstrip()
        if not os.path.exists('./' + active_rice):
            return (None, False, "Error, the .active file in the program rice folder is currently pointing to a non-valid rice, please change it to point to the rice that is currently being used")
        os.chdir('./' + active_rice)
        json_data = open('sysinfo.json')
        data = json.load(json_data)
        json_data.close()
        swfiles(data, './')
        swfiles(dict_file, './')
        return (active_rice, True, "")
    else:
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
