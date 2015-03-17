import os
import json
#TODO add hashing
def switch(prog_name, dict_file):
    os.chdir('~/.riceDB/' + prog_name)
    if(os.path.exists('./.active') and os.path.isfile('./.active')):
        #if rice is a riceDB rice, read sysinfo.json to move non-vanilla files
        active_rice = open('./.active').readline().rstrip()
        os.chdir('./' + active_rice)
        json_data = open('sysinfo.json')
        data = json.load(json_data)
        json_data.close()
        swfiles(data, './')
        swfiles(dict_file, './')
        return (active_rice,True,"")
    else:
        #else ask user for non-vanilla files
        user_files = {}
        another = 'y'
        while(another == 'y'):
            print("Please enter the path of your non-vanilla files:\n (type q to quit)")
            user_file = input()
            if os.path.isfile(user_file):
                t = os.path.split(user_file)
                user_files[t[1]]=(t[0] + '/')
                print("Do you have another non-vanilla file beside the ones you already typed in ? (y/n)")
                another = input().lower()
            elif(user_file == 'q'):
                return (None, False,"Exited due to user input")
            else:
                print("Filepath " + user_file + " is not valid, please retry.")
            print("Please choose a name for your personnal rice:")
            rice_name = input()
        while(os.path.exists('~/.riceDB/' + prog_name + '/' + rice_name)):
            print("A rice with this name already exists, please choose another name:")
            rice_name = input()
        os.mkdir(rice_name)
        swfiles(user_files,rice_name)
        swfiles(dict_file,'./')
        serialize(user_file,'sysinfo.json')
        return (rice_name,True,"")
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
        os.rename(dictionary[k] + k, './' + k)
