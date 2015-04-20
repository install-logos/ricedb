<h1 align="center">
<sub>
<img src="http://i.imgur.com/FvQ3Lvx.png"
      width="740">
      <img src="http://i.imgur.com/QR1AaJi.png"
      width="740">
</sub>
</h1>
<strong>RiceDB</strong> will be a universal configuration file manager 
designed to make it easy to obtain configurations for any application 
that fit your individual needs.

<strong>RiceDB</strong> seeks to follow the <strong>Arch Way</strong>, 
staying simple, open, and elegant.

###Requirements
Python3 - Possibly 2.7, but this has yet to be fully tested

###Installation
>git clone https://github.com/install-logos/ricedb.git

>cd ricedb

>make setup

>sudo make install

###Usage
To search for a rice for a program: rice [program] [search term]

To directly install a rice for a program: rice --sync [program] [name]

To create a registered rice from existing config files: rice --create [program]

To upload a rice to our database: rice --upload [program] [name] [URL to github repo]

IMPORTANT: For the above command to properly work, you should first initialize a repo in the folder ~/.rdb/[program]/[name] folder of the computer and upload it to github. You will then run this program once to generate metadata. Then enter into that folder, add the new info.json file and push it to your github. Then rerun this command to actually upload.

Please note our database is only populated with a few default rices, we are looking for people to help contribute to this


[![Build Status](https://travis-ci.org/install-logos/ricedb.svg?branch=master)](https://travis-ci.org/install-logos/ricedb)
[![Gitter 
chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/nih0/logos)
