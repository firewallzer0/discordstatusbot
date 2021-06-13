# Contributors
David R. Trask @firewallzer0

Ryan Chen @ryanscodebay

# Pre-requisites:
* centOS or RHEL 7 server to run on
* sudo or root access to that server
* influxdb installed
* python 3.6.8 or later
* pip installer
  * pip install discord
  * pip install influxdb
* Discord apibot key (https://discord.com/developers/applications)

# Task List
- [x] Basic Discord Bot that response to users and commands
- [ ] Poll Basic Server Stats
  - [ ] TrueNAS Basic Stats
  - [x] VMware Basic Stats
    - [ ] Number of powered on VMs
    - [x] Uptime
    - [x] Cluster CPU utilization
    - [x] Cluster RAM utilization
    - [x] Cluster Power usage  
  - [ ] pfSense Basic Stats
    - [ ] CPU utilization
    - [ ] Memory utilization
    - [ ] Bandwidth utilization
    - [x] (Run Speed Test and return results) OR (Get the latest results from scheduled script)
- [x] Write InfluxDB poller
- [x] Write webhook caller
- [x] Re-write to include json config file
- [ ] Finish writing instructions for the readme on configuring external components 

# How to use

## Install and configure the bot
   
**NOTE: For security reasons you will want to create a separate user account to run the bot. This is not necessary but highly recommended.**

*NOTE: For _ANY_ deviations, you will have to update the service file accordingly.*


1. Create a new user named _discord_ ```sudo adduser -M -s /bin/nologin discord```

2. Make the directoy __/opt/discordstausbot__ via the command: ```sudo mkdir /opt/discordstatusbot```

3. Change permissions on the __/opt/discordstatusbot__ folder to have discord be the owner via the command: ```sudo chown discord:discord /opt/discordstatusbot```

4. Become the discord user via the command: ```sudo su discord``` _NOTE: you may get an error that there is no home directory this is normal._

5. git clone to the folder ```git clone https://github.com/firewallzer0/discordstatusbot.git /opt/discordstatusbot```

6. Create latest.json and latest.sha256 ```cd /opt/discordstatusbot && touch latest.json && touch latest.sha256```
   
7. Copy the config.json.example to config.json ```cp config.json.example config.json```

8. Edit the file for your setup. 

9. Exit out of the discord user shell ```exit```

10. Copy __externalScripts/discordbot.service__ to __/usr/lib/systemd/system__ ```sudo cp /opt/discordstatusbot/externalScripts/discordbot.service /usr/lib/systemd/system/discordbot.service```

11. Reload systemD ```sudo systemctl daemon-reload```

12. Start the bot and enable start on boot ```sudo systemctl enable --now discordbot```

# Troubleshooting 
I recommend turning on debug in the config.json file, so you can see which call is causing the issue. Then check ```journalctl```

