#!/usr/bin/env bash
# run BlockChain Development Node
sudo /home/rajan/workarea/blockchain/appimage/ganache-1.2.2-x86_64.AppImage

# Flask run
FLASK_APP = app.py
FLASK_ENV = development
FLASK_DEBUG = 1
In folder /home/rajan/workarea/dlContract
/home/rajan/workarea/venv/dlContract/bin/python -m flask run
