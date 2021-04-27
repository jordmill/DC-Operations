import os
from webexteamsbot import TeamsBot
import requests
import json
from pytablewriter import MarkdownTableWriter
from contextlib import redirect_stdout
import urllib3
import io
from webexteamssdk import WebexTeamsAPI
from python_webex.v1.Bot import Bot
from python_webex import webhook
import emoji

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Retrieve required details from environment variables
bot_email = os.getenv("TEAMS_BOT_EMAIL")
teams_token = os.getenv("TEAMS_BOT_TOKEN")
bot_url = os.getenv("TEAMS_BOT_URL")
bot_app_name = os.getenv("TEAMS_BOT_APP_NAME")

# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
)

###############################################################################

te_token = ""#YOUR THOUSANDEYES OAUTH TOKEN
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer "+te_token,
}

params = {"aid": "200121"}

url = "https://api.thousandeyes.com/v6/alerts.json"

response = requests.get(url, headers=headers, params=params)

d = response.text

resp_dict = json.loads(d)

alert_info = resp_dict["alert"]

if len(alert_info) > 0:
    term_out = []

    # Opening markdown file and clearing it with print("") -> "print nothing"
    filename = "Thousandeyes_alerts.md"
    with open(filename, "w") as f:
        with redirect_stdout(f):
            print("")

    # Creating table name and column titles (headers)
    def main():
        writer = MarkdownTableWriter(
            table_name="",
            headers=[
                "Test Name",
                "                                                     ",
                "Timestamp",
                "                           ",
                "Issue",
                "                                             ",
                "Alert Rule",
                "                                                                                                                  ",
            ],
        )
        # writer.write_table()
        with open(filename, "a") as f:
            with redirect_stdout(f):
                print(writer)
                term_out.append(writer)

    main()

    for i in range(len(alert_info)):
        d = alert_info[i]
        g = d["ruleName"]
        j = d["testName"]
        aa = alert_info[i]
        ab = aa["agents"]
        ac = ab[0]
        ad = ac["metricsAtStart"]  # ISSUE
        af = ac["dateStart"]  # Timestamp
        # Setting up the rows to be populated with data. The spaces are important to line up with the headers (local int, forgein int, device id). the value matrix is from the parsing above and picks out desired values
        writer = MarkdownTableWriter(
            headers=[
                "                                         ",
                "                             ",
                "                                     ",
                "     ",
            ],
            value_matrix=[
                [j, af, ad, g],
            ],
        )
        # writer.write_table()

        # Writes data to markdown file

        with open(filename, "a") as f:
            with redirect_stdout(f):
                print(writer)
                term_out.append(writer)

    string = str(term_out)

    ff = string.replace(",", "")
    fs = ff.replace("|", "")

    final_table = fs[1:-1]

    # A simple command that returns a basic string that will be sent as a reply
    # def do_something(incoming_msg):
    def do_something():

        # return "i did what you said - {}".format(incoming_msg.text)

        api = WebexTeamsAPI()
        room_id = os.getenv("ROOM_ID")
        bot = Bot(os.getenv("TEAMS_BOT_TOKEN"))
        bot.create_webhook(
            name="quickstart_webhook",
            target_url=os.getenv("TEAMS_BOT_URL"),
            resource="messages",
            event="created",
        )

        bot.send_message(
            room_id=room_id,
            text=final_table,
            files=[
                "https://upload.wikimedia.org/wikipedia/commons/4/45/ThousandEyes-Logo.png",
            ],
        )

    do_something()

else:
    result = "No Alerts" + emoji.emojize(":white_check_mark:", use_aliases=True)
    # A simple command that returns a basic string that will be sent as a reply
    # def do_something(incoming_msg):
    def do_something():

        # return "i did what you said - {}".format(incoming_msg.text)

        api = WebexTeamsAPI()
        room_id = os.getenv("ROOM_ID")
        bot = Bot(os.getenv("TEAMS_BOT_TOKEN"))
        bot.create_webhook(
            name="quickstart_webhook",
            target_url=os.getenv("TEAMS_BOT_URL"),
            resource="messages",
            event="created",
        )

        bot.send_message(
            room_id=room_id,
            text=result,
            files=[
                "https://upload.wikimedia.org/wikipedia/commons/4/45/ThousandEyes-Logo.png",
            ],
        )

    do_something()
###############################################################################


# Add new commands to the box.
# bot.add_command("Any Alerts?", "help for do something", do_something)


if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)
