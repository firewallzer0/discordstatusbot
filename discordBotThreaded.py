# Import necessary libraries
import discord
import threading
import json
from discord.ext import commands
from datetime import datetime
from influxStatusListener import dbListener
from vmwareStatus import vmwareGetStatus
from getSpeedTest import getSpeedTest
from speedtest_import import importSpeedtest


########################################################################################################################
#                                      NEED TO ADD MORE VARIABLES aka debug setting passed to all sub-scripts
########################################################################################################################

debugFlag = False
botStartTime = datetime.now()

bot = discord.Client()
print('I: %s -- Main Thread -- Created bot client' % datetime.now())

# Prefix to be entered before commands
bot = commands.Bot(command_prefix='servers.')

##################
# Define Classes #
##################


class webhookThread(threading.Thread):
    def __init__(self):
        super(webhookThread, self).__init__()

    def run(self):
        dbListener()


class speedtestThread(threading.Thread):
    def __init__(self):
        super(speedtestThread, self).__init__()

    def run(self):
        importSpeedtest()


####################
# Define Functions #
####################

def validateJSON(jsonFile):
    try:
        jsonData = json.load(jsonFile)
    except ValueError as err:
        return [False, None]
    return [True, jsonData]


#########################
# Bot Command Functions #
#########################
@bot.command()
async def bottime(ctx):
    channel = bot.get_channel(ctx.channel.id)
    await channel.send("Bot has been running since: %s" % str(botStartTime))


@bot.command()
async def speedtest(ctx):
    channel = bot.get_channel(ctx.channel.id)
    user = bot.get_user(ctx.author.id)
    if debugFlag:
        print('D: %s -- Received the following command: "speedtest" from %s in channel %s' % (datetime.now(), user, channel))
    await channel.send(getSpeedTest())


@bot.command()
async def status(ctx):
    channel = bot.get_channel(ctx.channel.id)
    user = bot.get_user(ctx.author.id)
    if debug_Flag:
        print('D: %s -- Main Thread -- Received this info from ctx.channel.id: %s' % (datetime.now(), channel))
    vmwareStats = vmwareGetStatus()
    for eachStat in vmwareStats:
        await channel.send(eachStat)
    if debug_Flag:
        print('D: %s -- Main Thread -- Received the following command: "status" from %s in channel %s' % (datetime.now(), user, channel))
    else:
        print('I: %s -- Main Thread -- Received Request for Status' % datetime.now())


#######################
# Bot Event Functions #
#######################

@bot.event
async def on_ready():
    rightNow = datetime.now()
    print('I: %s -- Ready as {0.user}'.format(bot) % rightNow)
    readyChannel = bot.get_channel(announceChannel)
    await readyChannel.send('Server minions are online!')
    await bot.change_presence(activity=discord.Game(name=gameName))


@bot.event
async def on_disconnect():
    print("W: %s -- Main Thread -- Disconnected from Discord!" % datetime.now())


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if debug_Flag:
        channel = bot.get_channel(message.channel.id)
        print('D: %s -- Main Thread -- Received a message in channel: %s from %s' % (datetime.now(), channel, message.author.display_name))
    if message.content.startswith('Hello'):
       if message.author.id != ownerID:
            await message.channel.send('Hello %s you seem nice.' % message.author.display_name)
       else:
            await message.channel.send('Hello, master. We are here to serve.')

    await bot.process_commands(message)


@bot.event
async def on_connect():
    print('I: %s -- Main Thread -- Connected to Discord!' % datetime.now())

def main():


    ##########################
    # Initialize Discord Bot #
    ##########################

    print('I: %s -- Main Thread -- Opening and validating config file...' % datetime.now()) # Print console log
    try:    # Try opening the config file
        configFile = open('config.json', "r")

    except Exception:   # If it is not there
        print('E: %s -- Main Thread -- Unable to locate or read config.json...' % datetime.now())
        exit(1)     # End the program with a status code of 1


    isValidConfig, config = validateJSON(configFile)    # Check if the json is valid and get the dictionary passed back.

    if isValidConfig:
        pass    # If the JSON is valid do nothing
    else:
        print('E: %s -- Main Thread -- JSON invalid exiting...' % datetime.now()) 
        exit(1)



    ######################
    # Startup Variables  #
    ######################

    debugFlag = True
    # Store the bot version and release date
    ver = ['v0.1.0', '2020-12-24']
    apiKey = config['apiKey']

    announceChannel = int()
    ownerID = int()
    gameName = "Global Thermonuclear War"


    # Prefix to be entered before commands
    bot = commands.Bot(command_prefix='servers.')

    print('I: %s -- Main Thread -- Starting the webhook Thread...' % datetime.now())
    whThread = webhookThread()
    whThread.start()

    print('I: %s -- Main Thread -- Starting the speedtest Thread...' % datetime.now())
    spTestThread = speedtestThread()
    spTestThread.start()

    print('I: %s -- Main Thread -- Starting the Discord Bot Thread...' % datetime.now())
    bot.run(apiKey)
    print('I: %s -- Main Thread -- Kill signal received!' % datetime.now())


main()
