from rice import render, download, swapout, swapin
import json


def install(search_return, program_name):
    json_data = open('conf/index.json')
    data = json.load(json_data)
    json_data.close()

    if search_return is not None:
        selected_packs, render_success, render_message = render.select_options(search_return)
    else:
        print("Sorry, we could not find the rice or program of the specified name.")
        exit()

    if not selected_packs is None and render_success:
        for pack in selected_packs:
            rice_name = pack['Name']
            github_link = pack['Github Repository']
            vanilla_files = data.get(program_name, None)['Files']
        download_success, download_message = download.download(github_link, program_name, rice_name)
        if not download_success:
            print(download_message)
            exit()

        # Need to extract vanilla_files from the index.json to give to switchout and setup
        prev_rice, switchout_success, switchout_message = swapout.switch(program_name, vanilla_files)
        if not switchout_success:
            print(switchout_message)
            exit()

        swapin_success, swapin_message = swapin.install_rice(rice_name, program_name, vanilla_files)
        if not swapin_success:
            print(swapin_message)
            swapin.install_rice(prev_rice, program_name)
            exit()
    else:
        print(render_message)
        exit()
    print("Your rice for " + program_name + " has been succesfully installed. Reload the program to check it out")
