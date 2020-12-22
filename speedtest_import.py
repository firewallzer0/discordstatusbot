import json
from influxdb import InfluxDBClient
from datetime import datetime as dt



def importSpeedtest():

    debugSpeedtest = True
    pathTofile = 'example/example.json'
    pathToHash = '/opt/speedtest/latest.sha256'

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



    with open(pathTofile) as jsonFile:
        jsonData = json.load(jsonFile)
        print(jsonData)

    dbClient.close()


importSpeedtest()
