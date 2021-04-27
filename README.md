# How to Build a ChatOps Bot
This repo provides the required code, relating to the following articles, around - How to Build a ChatOps Bot.
* How to Build a Webex Teams Chatbot

## Load Environment Variable
Set your environment variables by copying the example `.env` and defining your settings.
Once done run `export $(cat .env | xargs)` to export your environment variables.
```
cp .env-example .env
```

## Create Environment
Next create a virtual environment and load your Python dependancies. 
```
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```


## Setup Ngrok
Download Ngrok into `/opt` via the instructions on https://dashboard.ngrok.com/get-started/setup.
Once done, set your auth token and start your Ngrok tunnel.
```
/opt/ngrok authtoken ${NGROK_TOKEN_ENV}
/opt/ngrok http -subdomain=chatop 5030
```

## Execute Chatbot
You can now start the Chatbot via:
```
python chatbot/webex_teams_bot2.py
```
