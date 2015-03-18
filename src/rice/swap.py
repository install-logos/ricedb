from rice import swapin, swapout
import json

def swap(program_name, rice_name):
    json_data = open("conf/index.json")
    data = json.load(json_data)
    json_data.close()
    vanilla_files = data.get(program_name, None)['Files']
    prev_rice, switchout_success, switchout_message = swapout.switch(program_name, vanilla_files)
    if not switchout_success:
        print(switchout_message)
        exit()
    swapin_success, swapin_message = swapin.install_rice(rice_name, program_name, vanilla_files)
    if not swapin_success:
        swapin.install_rice(prev_rice, program_name, vanilla_files)
        print(swapin_message)
        exit()
    print("The rice for " + program_name  + " has been switched to " + rice_name)
