#!/bin/bash
echo "Running git pull..."
/bin/git -c http.sslVerify=false pull
echo "Calling Python Script..."
/bin/python3 discordBotThreaded.py
