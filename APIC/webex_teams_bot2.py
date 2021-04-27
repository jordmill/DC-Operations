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
from contextlib import suppress
import emoji

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# getting apic cookie
cookie_url = "https://10.237.104.128/api/aaaLogin.json"

username = #APIC USERNAME
password = #APIC PASSWORD
cookie_payload = '{\n  "aaaUser":{\n    "attributes":{\n      "name":"apic:Local\\\\'+username+',\n      "pwd":'+password+'\n    }\n  }\n}'
cookie_headers = {
    "Content-Type": "application/json",
}

cookie_response = requests.request(
    "POST", cookie_url, headers=cookie_headers, data=cookie_payload, verify=False
)

raw = cookie_response.text.encode("utf8")
d = json.loads(raw)
da = d["imdata"]
db = da[0]
dc = db["aaaLogin"]
dd = dc["attributes"]
apic_cookie = dd["token"]  # APIC COOKIE


# Opening markdown file and clearing it with print("") -> "print nothing"
filename = "APIC_alerts.md"
with open(filename, "w") as f:
    with redirect_stdout(f):
        print("")


############################################################################################### CONTROLLER HEALTH

controller_term_out = []  # empty list that output will be added to

# Creating table name and column titles (headers)
def main():
    writer = MarkdownTableWriter(
        table_name="",
        headers=[
            "Node",
            "                                   ",
            "Admin State",
            "           ",
            "Op State",
            "         ",
            "Health",
            "   ",
        ],
    )
    # writer.write_table()
    with open(filename, "a") as f:
        with redirect_stdout(f):
            print(writer)
            controller_term_out.append(writer)


main()


# looping over APICs
Apics = [1, 2, 3]


for Apic in Apics:
    # makig request to APIC
    url = (
        "https://10.237.104.128/api/node/mo/topology/pod-1/node-"
        + str(Apic)
        + '.json?query-target=subtree&target-subtree-class=infraWiNode&query-target-filter=eq(infraWiNode.id,"'
        + str(Apic)
        + '")'
    )

    payload = {}
    headers = {"Cookie": "APIC-cookie=" + apic_cookie}

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    # parsing through output to get data
    output = response.text.encode("utf8")
    oa = json.loads(output)
    ob = oa["imdata"]
    oc = ob[0]
    od = oc["infraWiNode"]
    oe = od["attributes"]
    of = oe["nodeName"]  # NODE NAME
    og = oe["adminSt"]  # ADMIN STATE
    oh = oe["operSt"]  # OPERATIONAL STATE
    oi = oe["health"]  # HEALTH

    # Setting up the rows to be populated with data. The spaces are important to line up with the headers (local int, forgein int, device id). the value matrix is from the parsing above and picks out desired values
    if oi == "fully-fit":
        writer = MarkdownTableWriter(
            headers=[
                "                    ",
                "                ",
                "             ",
                "   ",
            ],
            value_matrix=[
                [
                    of + "         ",
                    og + "              ",
                    oh + "          ",
                    oi + emoji.emojize(":white_check_mark:", use_aliases=True),
                ],
            ],
        )
    else:
        writer = MarkdownTableWriter(
            headers=[
                "                    ",
                "                ",
                "             ",
                "   ",
            ],
            value_matrix=[
                [
                    of,
                    og,
                    oh,
                    oi + emoji.emojize(":large_orange_diamond:", use_aliases=True),
                ],
            ],
        )

    # writer.write_table()

    # Writes data to markdown file

    with open(filename, "a") as f:
        with redirect_stdout(f):
            print(writer)
            controller_term_out.append(writer)


############################################################################################### NODE HEALTH

node_term_out = []  # empty list that output will be added to

# Creating table name and column titles (headers)
def main1():
    writer = MarkdownTableWriter(
        table_name="",
        headers=[
            "Node",
            "                ",
            "Health score",
            "          ",
            "Check",
            "       ",
        ],
    )
    # writer.write_table()
    with open(filename, "a") as f:
        with redirect_stdout(f):
            print(writer)
            node_term_out.append(writer)


main1()

# looping over Nodes
Nodes = [
    "node-101",
    "node-102",
    "node-103",
    "node-104",
    "node-112",
    "node-113",
    "node-114",
    "node-115",
    "node-116",
    "node-121",
    "node-122",
    "node-123",
    "node-124",
    "node-125",
    "node-126",
    "node-201",
    "node-202",
]

for Node in Nodes:
    # makig request to Nodes
    url = (
        "https://10.237.104.128/api/node/mo/topology/pod-1/"
        + str(Node)
        + "/sys/HDfabricNodeHealth5min-0.json"
    )

    payload = {}
    headers = {"Cookie": "APIC-cookie=" + apic_cookie}

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    # parsing through output to get data
    output = response.text.encode("utf8")
    oa = json.loads(output)
    ob = oa["imdata"]
    oc = ob[0]
    od = oc["fabricNodeHealthHist5min"]
    oe = od["attributes"]
    health_score = oe["healthAvg"]  # HEALTH SCORE

    url = (
        "https://10.237.104.128/api/node/mo/topology/pod-1/"
        + Node
        + "/sys.json?query-target=children&rsp-subtree-include=health,fault-count"
    )
    payload = {}
    headers = {"Cookie": "APIC-cookie=" + apic_cookie}

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    ##############TRYING TO PUT ERROR REASON IF THERE IS ERROR

    # parsing through output to get data
    output = response.text.encode("utf8")
    oa = json.loads(output)
    ob = oa["imdata"]
    attribute_len = len(ob)

    if int(health_score) < 90:
        with suppress(Exception):
            for i in range(attribute_len):
                oc = ob[i]
                od = list(oc.keys())[0]  # Name of attribute
                oe = oc[od]
                of = oe["children"]
                if len(of) == 1:
                    og = of[0]
                    oh = og["faultCounts"]
                    oi = oh["attributes"]
                    oj = oi["crit"]
                    if oj == "1":
                        # Setting up the rows to be populated with data. The spaces are important to line up with the headers (local int, forgein int, device id). the value matrix is from the parsing above and picks out desired values
                        writer = MarkdownTableWriter(
                            headers=[
                                "          ",
                                "            ",
                                "                               ",
                            ],
                            value_matrix=[
                                [
                                    Node,
                                    "       "
                                    + health_score
                                    + emoji.emojize(
                                        ":large_orange_diamond:", use_aliases=True
                                    ),
                                    "                    " + od + "       ",
                                ],
                            ],
                        )
                        # writer.write_table()

                        # Writes data to markdown file

                        with open(filename, "a") as f:
                            with redirect_stdout(f):
                                print(writer)
                                node_term_out.append(writer)

                if len(of) == 2:
                    og = of[1]
                    oh = og["faultCounts"]
                    oi = oh["attributes"]
                    oj = oi["crit"]
                    if oj == "1":
                        # Setting up the rows to be populated with data. The spaces are important to line up with the headers (local int, forgein int, device id). the value matrix is from the parsing above and picks out desired values
                        writer = MarkdownTableWriter(
                            headers=[
                                "          ",
                                "            ",
                                "                               ",
                            ],
                            value_matrix=[
                                [
                                    Node,
                                    "       "
                                    + health_score
                                    + emoji.emojize(
                                        ":large_orange_diamond:", use_aliases=True
                                    ),
                                    "                    " + od + "       ",
                                ],
                            ],
                        )
                        # writer.write_table()

                        # Writes data to markdown file

                        with open(filename, "a") as f:
                            with redirect_stdout(f):
                                print(writer)
                                node_term_out.append(writer)

    else:

        # Setting up the rows to be populated with data. The spaces are important to line up with the headers (local int, forgein int, device id). the value matrix is from the parsing above and picks out desired values

        writer = MarkdownTableWriter(
            headers=["          ", "            ", "                               ",],
            value_matrix=[
                [
                    Node,
                    "       "
                    + health_score
                    + emoji.emojize(":white_check_mark:", use_aliases=True),
                    "                    Nothing to check!",
                ],
            ],
        )
        # writer.write_table()

        # Writes data to markdown file

        with open(filename, "a") as f:
            with redirect_stdout(f):
                print(writer)
                node_term_out.append(writer)


node_string = str(node_term_out)

ff = node_string.replace(",", "")
fs = ff.replace("|", "")

node_final_table = fs[1:-1]


controller_string = str(controller_term_out)

ff = controller_string.replace(",", "")
fs = ff.replace("|", "")

controller_final_table = fs[1:-1]
###############################################################################

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


# A simple command that returns a basic string that will be sent as a reply
# def do_something(incoming_msg):
def do_something():

    # return "i did what you said - {}".format(incoming_msg.text)

    api = WebexTeamsAPI()
    room_id = os.getenv("ROOM_ID")
    bot = Bot(os.getenv("TEAMS_BOT_TOKEN"))
    bot.create_webhook(
        name="quickstart_webhook",
        target_url="http://a02c3bee6fc3.ngrok.io",
        resource="messages",
        event="created",
    )
    bot.send_message(
        room_id=room_id,
        text="\n{}".format(controller_final_table),
        files=["https://store.servicenow.com/7a3e80b4db8df7089e7f56a8dc961927.iix",],
    )
    bot.send_message(
        room_id=room_id, text="\n{}".format(node_final_table),
    )


do_something()

# Add new commands to the box.
# bot.add_command("Any Alerts?", "help for do something", do_something)


if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)
