# Import necessary libraries
import discord
import threading
from discord.ext import commands
from datetime import datetime

debug_Flag = True
# Store the bot version and release date
ver = ['v0.0.1', '2020-12-17']

botStartTime = datetime.now()
print('I: %s -- Starting bot...' % botStartTime)

bot = discord.Client()
print('I: %s -- Created bot client' % datetime.now())

# Prefix to be entered before commmands
bot = commands.Bot(command_prefix='servers.')


########################
# Bot Commands Section #
########################
@bot.command()
async def test(ctx):
    if debug_Flag:
        print('D: %s -- Received Test Command!' % datetime.now())
    pass


@bot.command()
async def status(ctx):
    channel = bot.get_channel(ctx.channel.id)
    user = bot.get_user(ctx.author.id)
    if debug_Flag:
        print('D: %s -- Received this info from ctx.channel.id: %s' % (datetime.now(), channel))
    await channel.send('Some Made Up Stats....')
    time = datetime.now()
    if debug_Flag:
        print('D: %s -- Received the following command: "status" from %s in channel %s' % (time, user, channel))
    else:
        print('I: %s -- Received Request for Status' % time)


######################
# Bot Events Section #
######################

@bot.event
async def on_ready():
    rightNow = datetime.now()
    print('I: %s -- Ready as {0.user}'.format(bot) % rightNow)
    readyChannel = bot.get_channel(616348858972242012)
    # await readyChannel.send('Server Minions are Online!')


@bot.event
async def on_connect():
    rightNow = datetime.now()
    print('I: %s -- Connected!' % rightNow)


@bot.event
async def on_disconnect():
    rightNow = datetime.now()
    print("W: %s -- Disconnected!" % rightNow)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if debug_Flag:
        channel = bot.get_channel(message.channel.id)
        print('D: %s -- Received a message in channel: %s from %s' % (
        datetime.now(), channel, message.author.display_name))

    if message.content.startswith('Hello'):
        if message.author.id == 172064604942237697:
            await message.channel.send('Hey, fuck you buddy, stop repressing me. You communist swine!')
        elif message.author.id == 188448821565456384:
            await message.channel.send('Hello, master. We are here to serve.')
        elif message.author.id == 133243837555408898:
            await message.channel.send('Hey %s my man. *finger guns*' % message.author.display_name)
        else:
            await message.channel.send('Hello %s' % message.author.display_name)

    if message.channel.id == 616348858972242012:
        print('D: %s -- Received the following message: %s'.format(bot) % (datetime.now(), message.content))

    await bot.process_commands(message)


# Load API key from external file
apiKey = open("../keys/api.key", "r").read()
bot.run(apiKey)
