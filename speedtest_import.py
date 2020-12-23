import json
from influxdb import InfluxDBClient
from datetime import datetime as dt
import hashlib
from time import sleep


def importSpeedtest():
    debugSpeedtest = False
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
        if debugSpeedtest:  # Debug console logging
            print('D: %s -- Hashes are the same...' % (str(dt.now())))  # Debug console logging

        oldHash.close()
    else:
        if debugSpeedtest:  # Debug console logging
            print('D: %s -- Hashes are the different...' % (str(dt.now())))  # Debug console logging

        # print(hashedJson)
        # print(oldHash)
        if debugSpeedtest:  # Debug console logging
            print('D: %s -- Deleting old hash and writing new one...' % (str(dt.now())))
        oldHash.truncate(0)
        oldHash.write(hashedJson)
        oldHash.close()
        if debugSpeedtest:  # Debug console logging
            print('D: %s -- Getting data we care about...' % (str(dt.now())))
        download = round(jsonData['download'])
        upload = round(jsonData['upload'])
        ping = jsonData['ping']
        isp = jsonData['client']['isp']
        host = jsonData['server']['sponsor']
        time = jsonData['timestamp']
        if debugSpeedtest:  # Debug console logging
            print('D: %s -- Building new JSON in memory...' % (str(dt.now())))
        jsonBuilder = json.loads(
            '{"measurement": "network_stats","tags": {"isp": "%s"},"fields": {"download": "%d", "upload": "%d", "ping": "%.2f", "host": "%s", "time": "%s"}}' % (
            isp, download, upload, ping, host, str(time)))
        builderList = [jsonBuilder]
        if debugSpeedtest:  # Debug console logging
            print('D: %s -- Passing new JSON/List to database...' % (str(dt.now())))
        dbClient.write_points(builderList, database=dbName)

    print('I: %s -- Closing database connection...' % (str(dt.now())))
    dbClient.close()


def main():
    while True:
        print('I: %s -- Waking up and calling function' % str(dt.now()))
        importSpeedtest()
        print('I: %s -- Sleeping for 5 minutes...' % (str(dt.now())))
        sleep(300)


main()
