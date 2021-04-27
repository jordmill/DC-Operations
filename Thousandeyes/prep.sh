#!/bin/bash

cd <your chosen path>/Thousandeyes
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt

export TEAMS_BOT_URL=#NGROK_URL
export TEAMS_BOT_TOKEN=#WEBEX_BOT_TOKEN
export TEAMS_BOT_EMAIL=#WEBEX_BOT_URL
export TEAMS_BOT_APP_NAME=#WEBEX_BOT_USERNAME
export ROOM_ID=#WEBEX_ROOM_ID
set auth_token=#WEBEX_BOT_TOKEN
export WEBEX_TEAMS_ACCESS_TOKEN=#WEBEX_BOT_TOKEN

python webex_teams_bot2.py
