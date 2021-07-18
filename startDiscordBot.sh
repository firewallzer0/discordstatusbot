#!/bin/bash

# This first step is not needed, I am using it to make sure the bot is up to date by pulling from a private git repo.
# Though I should move this over to pulling from github at some point, but this is for internal testing.
# I'll make like 12 updates for simple syntax issues, and this is my way of seeming competent.

echo "Running git pull..."
/bin/cd /opt/discordstatusbot && /bin/git -c http.sslVerify=false pull


echo "Calling Python Script..."
/bin/python3 /opt/discordstatusbot/discordBotThreaded.py
