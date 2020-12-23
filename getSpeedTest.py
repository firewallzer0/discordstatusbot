from influxdb import InfluxDBClient
from datetime import datetime as dt

debugGetSpeedTest = True


def getSpeedTest():

    if debugGetSpeedTest:  # Debug console logging
        print('D: %s -- Initializing for database connection...' % str(dt.now()))  # Debug console logging

    dbUser = 'statsbot'  # Set database user
    dbPassword = open("keys/statsDBpassword.key", "r").read()  # Retrieve database password from file
    dbHostname = '10.10.10.77'  # Change to your database's IP or host name
    dbPort = 8086  # Change to your database's port; Default is 8086
    dbName = 'speed-test'  # Change to the name of the database you want to work on

    print('I: %s -- Creating connection to database...' % str(dt.now()))  # Console logging
    dbClient = InfluxDBClient(host=dbHostname, port=dbPort, username=dbUser, password=dbPassword)  # Connect to database

    if debugGetSpeedTest:  # Debug console logging
        print('D: %s -- Switching to %s database...' % (str(dt.now()), dbName))  # Debug console logging

    dbClient.switch_database('%s' % dbName)  # Select the database you what to use.

    if debugGetSpeedTest:  # Debug console logging
        print('D: %s -- Querying the %s database...' % (str(dt.now()), dbName))  # Debug console logging

    results = dbClient.query('SELECT last(*) FROM network_stats')
    for result in results:  # There is only 1 set this is a hack to pull a layer off
        if debugGetSpeedTest:  # Debug console logging
            print('D: %s -- For result in results...' % str(dt.now()))  # Debug console logging

        download = int(result[0]['last_download'])
        upload = int(result[0]['last_upload'])
        ping = float(result[0]['last_ping'])
        host = result[0]['last_host']

        download = round(download / 1000 / 1000)
        upload = round(upload / 1000 / 1000)

        message = "Download Speed is: %d Megabits per second\nUpload Speed is: %d Megabits per second\nCurrent ping time is: %f milliseconds\nLast test was against: %s" % (download, upload, ping, host)
        #print(message)
        return message
