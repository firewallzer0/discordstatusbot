#!/bin/bash
echo "Running git pull..."
/bin/cd /opt/discordstatusbot && /bin/git -c http.sslVerify=false pull
echo "Calling Python Script..."
/bin/python3 /opt/discordstatusbot/discordBotThreaded.py
