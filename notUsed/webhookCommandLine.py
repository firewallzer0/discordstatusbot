import json
import sys
import requests


url = open(str(sys.argv[1]), "r").read()
message = str(sys.argv[2])

discord_data = {
    "content": message
}
byte_length = str(sys.getsizeof(discord_data))
headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
response = requests.post(url, data=json.dumps(discord_data), headers=headers)
if response.status_code != 204:
    raise Exception(response.status_code, response.text)
