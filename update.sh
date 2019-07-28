#!/bin/bash
uwsgi=uwsgi@social.service

sudo systemctl stop $uwsgi
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo systemctl start $uwsgi
