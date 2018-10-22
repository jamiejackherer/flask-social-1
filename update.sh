#!/bin/bash
sudo systemctl stop uwsgi
source env/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo systemctl start uwsgi
