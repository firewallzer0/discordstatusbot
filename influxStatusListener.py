from influxdb import InfluxDBClient
from time import sleep
from datetime import datetime as dt
import hashlib
from webhookFunction import discordWebhook as webhook

######################
# Main function loop #
######################
def dbListener():

    #######################
    # Configure variables #
    #######################
    mention = True  # Change to True if you'd like the notice to mention a user
    debugDBListner = True  # Change to True to see debugging logs
    timer = 15  # How frequently to poll in seconds
    relativeTime = '5m'  # How far back in the database to look m=minutes, h=hours, d=days, w=weeks
    series = 'Notifications'  # Name of the series you'd like to search through

    if mention:
        user = str(open("/opt/discordstatusbot/keys/myUserID.key", "r").read())  # Change to your user ID as a string or call from file
    else:
        user = None

    ############################
    # Setup for database calls #
    ############################

    if debugDBListner:  # Debug console logging
        print('D: %s -- Status Listener -- Initializing for database connection...' % str(dt.now()))  # Debug console logging
    dbUser = open("/opt/discordstatusbot/keys/dbUser.key", "r").read()  # Retrieve database user from file
    dbPassword = open("/opt/discordstatusbot/keys/dbPassword.key", "r").read()  # Retrieve database password from file
    dbHostname = '10.10.10.171'  # Change to your database's IP or host name
    dbPort = 8086  # Change to your database's port; Default is 8086 for influxdb
    dbName = 'truenas'  # Change to the name of the database you want to work on

    print('I: %s -- Status Listener -- Creating connection to database...' % str(dt.now()))  # Console logging

    dbClient = InfluxDBClient(host=dbHostname, port=dbPort, username=dbUser, password=dbPassword)  # Connect to database
    if debugDBListner:  # Debug console logging
        print('D: %s -- Status Listener -- Switching to %s database...' % (str(dt.now()), dbName))  # Debug console logging
    dbClient.switch_database('%s' % dbName)  # Select the database you what to use.

    # hashedData = 0  # Initialize default values
    oldHash = 0  # Initialize default values



    while True:                                                     # Always do this
        results = dbClient.query('SELECT * FROM %s WHERE time > now() - %s' % (series, relativeTime))   # Database Query
        hashCoding = str(results)                                   # Convert the ResultSet into a string
        hashedData = hashlib.sha1(hashCoding.encode('utf-8')).hexdigest()   # Hash the string, so we can compare it later
        if oldHash == hashedData:                                   # If hashes are equal do nothing
            if debugDBListner:
                print('D: %s -- Status Listener -- Hashes are equal, doing nothing...' % str(dt.now()))
            pass                                                    # Doing nothing
        else:
            oldHash = hashedData                                    # Since the hashes weren't equal, make them equal now.
            if debugDBListner:                                                               # Debug console logging
                print('D: %s -- Status Listener -- Hashes are not equal...' % str(dt.now()))           # Debug console logging
            for result in results:                                  # There is only 1 set this is a hack to pull a layer off
                if debugDBListner:                                                           # Debug console logging
                    print('D: %s -- For result in results...' % str(dt.now()))      # Debug console logging
                for i in range(len(result)):                        # Get the total number of lists in the result and loop
                    data = []                                       # Clear our data from the list for the next loop
                    for item in result[i].items():                  # Getting the item from the list of lists
                        if debugDBListner:
                            print('D: %s -- Status Listener -- For item in result[%d].items()...' % (str(dt.now()), i))  # Debug console logging
                            print('D: %s -- Status Listener -- For item append data...' % str(dt.now()))   # Debug console logging

                        data.append(str(item[1]))                   # Add to the list the key value
                    if debugDBListner:                                                       # Debug console logging
                        print('D: %s -- Status Listener -- Building notice...' % str(dt.now()))        # Debug console logging

                    notice = str('Notice: \n At %s: \n %s' % (data[0], data[1]))    # Build a message with the values
                    print('I: %s -- Status Listener -- Calling webhook... \n %s' % (str(dt.now()), notice))    # Console logging

                    # Call the webhook passing the address from file and the message built above and the user to mention
                    url = open("/opt/discordstatusbot/keys/discordWebHook-serversStatusChannel.key", "r").read()
                    webhook(url=str(), message=notice, discordUser=user)
        if debugDBListner:                                                                   # Debug console logging
            print('D: %s -- Status Listener -- Sleeping for %d seconds...' % (str(dt.now()), timer))   # Debug console logging
        sleep(timer)                                                # How often do you want to poll the database? Set above
