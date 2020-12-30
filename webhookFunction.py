import json
import sys
import requests


def discordWebhook(url, message, discordUser=None):
    if message == "":
        return 1
    if message is None:
        return 1

    if discordUser is not None:
        discord_data = {
            "content": "<@%s> \n %s: " % (discordUser, message)
        }
    else:
        discord_data = {
            "content": "%s: " % message
        }

    byte_length = str(sys.getsizeof(discord_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}

    response = requests.post(url, data=json.dumps(discord_data), headers=headers)
    if response.status_code != 204:
        raise Exception(response.status_code, response.text)
        return 2

