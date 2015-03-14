#TODO:
##Client-DL Interactions:
1. json parser
2. (@potsmodern)check installed software and save to ~/.ricebowl/config.yml
3. image gallery viewer
4. backup files - the program will basically have easy theme switching so by install
    use a .ricebowl/[configname]-ricedb folder to store alternative themes not being used
    installing a new theme will put the current theme into this folder and there will be
    a simple command to switch between current theme and the ones in the folder
5. Know where each program's configs are - this will be in the github repos index
6. Allow dotfile repo creators to require dependancies for their dotfiles

##CLIENT-UL Interactions:
1. Setup packaging standards.
     ie. each repo must contain pictures of rice and a file outlining required dependancies that the ricer program can parse, in addition to breif descriptions, as from pacman.

##CLIENT -> SERVER UL Interactions:
1. Account creation to verify that you are a human not a bot - to upload a config you must login, but you don't have to tie the upload to your account
2. Account verification - need to securely process requests from clients to upload
3. Client upload verification - ensure this isn't a duplicate or plagiarised or otherwise spam
4. github repo creation - use github API to package the files with an index that clients will use to know how to install the files
5. Web frontend with URI linking as an alternative to the CLI

##SERVER -> CLIENT DL Interactions:
1. Enable easy download updated index files, and sending notifications to clients about new updates
2. Simple means to refresh and update the directories and other attributes of the config loader.

##Misc scripts:
1. serverside testing suite: check if compiles

##Formatting:
1. Index files: Have one overall index file or multiple files
2. Multi file - One primary index that lists all software and some data about them and secondary index files for each piece of software that contains the specific details about each rice.
3. Secondary index files will follow a [name] [description] [images] [github repo] format - possibly include author
