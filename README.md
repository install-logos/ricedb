# How to get this running

## Make ~/.rdb

Copy `config` to `~/.rdb/config`

## Run a local server on port 8000

Run `python -m http.server` in the `riceDB` directory of this repo.  This serves up `test.zip` and simulates the "upstream".

## Run another local server on port 9000

Run `python server.py`.

## Try out rice.py

`cd src; python rice.py`

Type something and hit enter.
