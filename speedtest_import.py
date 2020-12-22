import json
from influxdb import InfluxDBClient
from datetime import datetime as dt
import hashlib


def importSpeedtest():

    debugSpeedtest = True
    pathTofile = 'example/example.json'
    pathToHash = 'example/latest.sha256'

    ############################
    # Setup for database calls #
    ############################

    if debugSpeedtest:  # Debug console logging
        print('D: %s -- Initializing for database connection...' % str(dt.now()))  # Debug console logging

    dbUser = 'statsbot'  # Set database user
    dbPassword = open("keys/statsDBpassword.key", "r").read()  # Retrieve database password from file
    dbHostname = '10.10.10.77'  # Change to your database's IP or host name
    dbPort = 8086  # Change to your database's port; Default is 8086
    dbName = 'speed-test'  # Change to the name of the database you want to work on

    print('I: %s -- Creating connection to database...' % str(dt.now()))  # Console logging
    dbClient = InfluxDBClient(host=dbHostname, port=dbPort, username=dbUser, password=dbPassword)  # Connect to database

    if debugSpeedtest:  # Debug console logging
        print('D: %s -- Switching to %s database...' % (str(dt.now()), dbName))  # Debug console logging

    dbClient.switch_database('%s' % dbName)  # Select the database you what to use.

    if debugSpeedtest:  # Debug console logging
        print('D: %s -- Opening JSON...' % (str(dt.now())))  # Debug console logging

    with open(pathTofile) as jsonFile:
        jsonData = json.load(jsonFile)
    if debugSpeedtest:  # Debug console logging
        print('D: %s -- Opened JSON, now hashing...' % (str(dt.now())))  # Debug console logging
    hashedJson = hashlib.sha1(str(jsonData).encode('utf-8')).hexdigest()

    if debugSpeedtest:  # Debug console logging
        print('D: %s -- Comparing Hashes...' % (str(dt.now())))  # Debug console logging

    oldHash = open(pathToHash, "r+")
    if (oldHash.read()) == hashedJson:
        print(hashedJson)
        oldHash.close()
    else:
        print(hashedJson)
        print(oldHash)
        oldHash.truncate(0)
        oldHash.write(hashedJson)
        oldHash.close()
        dbClient.write_points(jsonData,database=dbName)





    dbClient.close()
#    download = round(jsonData['download'])
#    upload = round(jsonData['upload'])
#    ping = jsonData['ping']
#    isp = jsonData['client']['isp']
#    print("%.2f" %download)

importSpeedtest()
