#!/usr/bin/python
from rice import search
# from rice import render
# from rice import download
# from rice import switch
# from rice import setup

import argparse

# Main Script for running riceDB
# To install a new rice, rice.py will:
# Search for the specified rice/software using the search lib
# Process the results of the search call, organizing by a criteri
# such as popularity
# Call the rendering library which will take the sorted list and
# display the options to the user, as well as a way for the user
# to select a rice of their choosing
# Render.py should take a json and a string as arguments,
# and will render the json in a predetermined format and display
# the string at the bottom. It will also return the users input
# to the rice method, which will be the rice the user wants
# Rice.py will then call the download library which will fetch
# the github repo specified in the selected rice, unpack it
# into a new folder within the .[program-name]-rice folder,
# assuming that it doesn't already exist
# Rice.py will call the inspection library - this will look for
# existing configuration files for the software present in the system
# and their origin
# If the currently installed rice is from riceDB, it will run the
# Switchout.py script and move the files into the folder in the
# .[program-name]-rice folder in the users home directory
# Note: Read the wiki on config switching for more details about this
# In the event that the current config is not from riceDB, Switchout.py
# will ask the user for the name of their current configuration
# Switchout.py then creates a folder in the .[program-name]-rice folder
# that has the user specified name(assuming that the folder is valid
# and doesn't already exist). All default config files will be moved
# into this folder and the user will be asked for nondefault configuration
# files which may be part of the current rice. The user will specify
# the full path of these files and their name and this will be used to
# generate a sysinfo.json and move the respective files into the created
# folder.
# Rice.py then will call the setup library which will take arguments
# of a sysinfo.json, and a dictionary(of file names/locations) extracted from json.index.
# These will contain entries in the format: 
# configname:location and Setup.py will move all config names specified in these two
# inputs to their respective locations
# Setup.py will finally modify the 'active' file in the .[programname]-rice
# directory to point to the correct folder
# Rice.py will now be completed and exit

# SUMMARY OF PROCESS:
# Rice.py calls Search.py which returns a JSON
# Rice.py processes this JSON and calls Render.py
# Rice.py calls Download.py to download selected rice
# Rice.py calls Switchout.py to move out the current configs
# Rice.py calls Setup.py to move files into correct locations
# Rice.py exits

parser = argparse.ArgumentParser(description='RiceDB cmdline cli')
parser.add_argument('program', help='program to rice')
parser.add_argument('rice', nargs='?', help='rice package')
parser.add_argument('-S', '--sync',
                    help='Install a package directly.')
search_return = []
selected_pack = None
rice_name, program_name, github_link = ""
args = parser.parse_args()
if args.sync:
    search_return = search.search_packages(args.program, args.sync, search.get_package)

elif args.rice:
    search_return = search.search_packages(args.program, args.rice, search.search_keywords)

else:
    search_return = search.get_software(args.program))

if not search_return is None:
	selected_pack = render.select_options(search_return)
else:
	render.no_results()
	exit()
if not selected_pack is None:
	rice_name = selected_pack['Name']
	github_link = selected_pack['Github Repository']
	program_name = args.program
else:
	print("Error, render failed to return a valid result")
	exit()

download_success = download.get_rice(rice_name,program_name,github_link)
if not download_success:
	print("Error, the rice you have tried to download has a naming conflict with a pre-existing rice")
	exit()

prev_rice, switchout_success = switchout.switch(program_name)
if not switchout_success:
	print("Sorry, we could not succesfully swap out the rice that is currently installed")
	exit()

setup_success = setup.install_rice(rice_name,program_name)
if not setup_success:
	print("Sorry, the rice you want to install could not be properly setup")
	setup.install_rice(prev_rice, program_name)
	exit()

print("Your rice for " + program_name + " has been succesfully installed. Reload the program to check it out")
