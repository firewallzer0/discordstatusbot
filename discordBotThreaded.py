# Import necessary libraries
import discord
import threading
from discord.ext import commands
from datetime import datetime
from influxStatusListener import dbListener
from vmwareStatus import vmwareGetStatus
from getSpeedTest import getSpeedTest
from speedtest_import import importSpeedtest
from validateJSON import validateJSON

###########################
# Startup Initialization  #
###########################

print('I: %s -- Main Thread -- Initializing Discord Status Bot...' % datetime.now())  # Print console log
print('I: %s -- Main Thread -- Opening config file...' % datetime.now())  # Print console log

try:
    configFile = open('config.json', "r")   # Try opening the config file

except Exception:  # If it is not there
    print('E: %s -- Main Thread -- Unable to locate or read config.json...' % datetime.now())
    exit(1)  # End the program with a status code of 1

isValid, config = validateJSON(configFile)  # Check if the json is valid

if isValid:
    pass
else:
    print('E: %s -- Main Thread -- invalid JSON look at message above for exact error...' % datetime.now())
    exit(1)

######################
# Startup Variables  #
######################
print('I: %s -- Main Thread -- Assigning config file variables...' % datetime.now())  # Print console log
botVersion = ['v0.1.0', '2020-12-24']  # Store the bot version and release date
configVersion = config['configVersion']
debugFlag = config['debug']
apiKey = config['apiKey']
ownerID = int(config['ownerID'])
announceChannel = int(config['announcementChannelID'])
if config['gameName'] is not None:
    gameName = config['gameName']
botStartTime = datetime.now()
bot = discord.Client()
print('I: %s -- Main Thread -- Created bot client' % datetime.now())
# Prefix to be entered before commands
bot = commands.Bot(command_prefix=config['commandPrefix'])  # Prefix to be entered before commands


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

#########################
# Bot Command Functions #
#########################
@bot.command()
async def bottime(ctx):
    channel = bot.get_channel(ctx.channel.id)
    await channel.send("Bot has been running since: %s" % str(botStartTime))


@bot.command()
async def botversion(ctx):
    channel = bot.get_channel(ctx.channel.id)
    await channel.send('Bot version is %s\nConfig version is %s' % botVersion, configVersion)


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
    if debugFlag:
        print('D: %s -- Main Thread -- Received this info from ctx.channel.id: %s' % (datetime.now(), channel))
    vmwareStats = vmwareGetStatus()
    for eachStat in vmwareStats:
        await channel.send(eachStat)
    if debugFlag:
        print('D: %s -- Main Thread -- Received the following command: "status" from %s in channel %s' % (
        datetime.now(), user, channel))
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
    if config['gameName'] is not None:
        await bot.change_presence(activity=discord.Game(name=gameName))


@bot.event
async def on_disconnect():
    print("W: %s -- Main Thread -- Disconnected from Discord!" % datetime.now())


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if debugFlag:
        channel = bot.get_channel(message.channel.id)
        print('D: %s -- Main Thread -- Received a message in channel: %s from %s' % (
        datetime.now(), channel, message.author.display_name))
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

    print('I: %s -- Main Thread -- Starting the webhook Thread...' % datetime.now())
    whThread = webhookThread()
    whThread.start()

    if config['speedTestDB'] != '':
        print('I: %s -- Main Thread -- Starting the speedtest Thread...' % datetime.now())
        spTestThread = speedtestThread()
        spTestThread.start()
    else:
        print('I: %s -- Main Thread -- No speed test database was provided skipping thread...' % datetime.now())

    print('I: %s -- Main Thread -- Starting the Discord Bot Thread...' % datetime.now())
    bot.run(apiKey)
    print('I: %s -- Main Thread -- Kill signal received!' % datetime.now())


main()
