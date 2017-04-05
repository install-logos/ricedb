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

### Requirements
Python3 - Possibly 2.7, but this has yet to be fully tested

### Installation
    git clone https://github.com/install-logos/ricedb.git

    cd ricedb

    make config

    sudo make install

### Usage
To search for a rice for a program: `rice [program] [search term]`

To directly install a rice for a program: `rice --sync [program] [name]`

To create a registered rice from existing config files: `rice --create [program]`

To upload a rice to our database: `rice --upload [program] [name]`

Please note, the uploading functionality requires you to have a github account. A repo for the rice will be automatically created, you simply need an existing github account.

Please note our database is only populated with a few default rices, we are looking for people to help contribute to this


[![Build Status](https://travis-ci.org/install-logos/ricedb.svg?branch=master)](https://travis-ci.org/install-logos/ricedb)
[![Gitter 
chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/nih0/logos)
[![QuantifiedCode](https://www.quantifiedcode.com/api/v1/project/7a5332abe0bb46d2b7f84faf94028fc5/badge.svg)](https://www.quantifiedcode.com/app/project/7a5332abe0bb46d2b7f84faf94028fc5)
