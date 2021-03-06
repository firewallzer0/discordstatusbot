from influxdb import InfluxDBClient
from datetime import datetime as dt
import time
import json


def vmwareGetStatus():

    configFile = open('config.json', "r")   # Open config.json file for reading
    config = json.load(configFile)      # Load json data into memory
    configFile.close()      # Close config.json file

    #######################
    # Configure variables #
    #######################
    debugVMwareStatus = config['debug']  # Change to True to see debugging logs

    ############################
    # Setup for database calls #
    ############################

    if debugVMwareStatus:  # Debug console logging
        print('D: %s -- vmwareStatus -- Initializing for database connection...' % str(dt.now()))  # Debug console logging

    dbUser = config['dbUser']  # Set database user
    dbPassword = config['dbPassword']  # Retrieve database password from file
    dbHostname = config['dbHost']  # Change to your database's IP or host name
    dbPort = config['dbPort']  # Change to your database's port; Default is 8086
    dbName = config['vmwareStatsDB']  # Change to the name of the database you want to work on

    print('I: %s -- vmwareStatus -- Creating connection to database...' % str(dt.now()))  # Console logging

    dbClient = InfluxDBClient(host=dbHostname, port=dbPort, username=dbUser, password=dbPassword)  # Connect to database

    if debugVMwareStatus:  # Debug console logging
        print('D: %s -- vmwareStatus -- Switching to %s database...' % (str(dt.now()), dbName))  # Debug console logging

    dbClient.switch_database('%s' % dbName)  # Select the database you what to use.

    percentSign = chr(37)
    pwrMessageESX01 = None
    pwrMessageESX02 = None

    print('I: %s -- vmwareStatus -- Querying database now...' % str(dt.now()))  # Console logging

    cpuResults = dbClient.query('SELECT percentile("usage_average", 95) FROM "vsphere_host_cpu" WHERE (time >= now() - 30m)')  # Database Query
    # cpuResults = dbClient.query('SELECT percentile("usage_average", 95) FROM "vsphere_host_cpu" WHERE (esxhostname = \'10.1.1.9\') AND (time >= now() - 30m)')  # Database Query
    for cpuUsage in cpuResults:
        clusterCPUusage = str(cpuUsage[0]["percentile"])
        cpuMessage = 'CPU usage is: %s%s' % (clusterCPUusage, percentSign)

    ramResults = dbClient.query('SELECT last("usage_average") FROM "vsphere_host_mem" WHERE time >= now() - 30m AND "last" != "None" GROUP BY time(1m)')  # Database Query
    for ramUsage in ramResults:
        # print(ramUsage)
        clusterRAMusage = str(ramUsage[1]["last"])
        ramMessage = 'RAM usage is: %s%s' % (clusterRAMusage, percentSign)

    pwrResultsESX01 = dbClient.query('SELECT mean("power_average") AS "Watts" FROM "vsphere_host_power" WHERE ("esxhostname" = \'10.1.1.7\' AND time >= now() - 30m)')  # Database Query
    for pwrUsageESX01 in pwrResultsESX01:
        clusterPWRusageESX01 = str(round(pwrUsageESX01[0]["Watts"]))
        pwrMessageESX01 = ('Power usage for ESX01 is: %s Watts' % clusterPWRusageESX01)

    pwrResultsESX02 = dbClient.query('SELECT mean("power_average") AS "Watts" FROM "vsphere_host_power" WHERE ("esxhostname" = \'10.1.1.9\' AND time >= now() - 30m)')  # Database Query
    for pwrUsageESX02 in pwrResultsESX02:
        clusterPWRusageESX02 = str(round(pwrUsageESX02[0]["Watts"]))
        pwrMessageESX02 = ('Power usage for ESX02 is: %s Watts' % clusterPWRusageESX02)

    uptimeResults = dbClient.query('SELECT last("uptime_latest") AS "Uptime" FROM "vsphere_host_sys" WHERE time >= now() - 30m')
    for totalUptime in uptimeResults:
        uptimeValue = int(totalUptime[0]["Uptime"])
        seconds = uptimeValue % (10 * 52 * 7 * 24 * 3600)   # 10 years, 52 weeks, 7 days, 24 hours, 3600 seconds
        weeks = seconds // (7 * 24 * 3600)
        seconds %= (7 * 24 * 3600)
        days = seconds // (24 * 3600)
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        epochTime = int(time.time())
        startUptime = epochTime - uptimeValue
        startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startUptime))
        uptimeMessage = "The servers has been up for %d week(s), %d day(s), %d hour(s), %d minute(s), %d second(s)" % (weeks, days, hours, minutes, seconds)
        startMessage = "The servers have been up since: %s" % startTime


    print('I: %s -- vmwareStatus -- Returning stats...' % str(dt.now()))  # Console logging
    if pwrMessageESX01 == None:
        if pwrMessageESX02 == None:
            return [startMessage, cpuMessage, ramMessage, uptimeMessage]
        else:
            return [startMessage, cpuMessage, ramMessage, pwrMessageESX02, uptimeMessage]
    else:
        if pwrMessageESX02 == None:
            return [startMessage, cpuMessage, ramMessage, pwrMessageESX01, uptimeMessage]
        else:
            return [startMessage, cpuMessage, ramMessage, pwrMessageESX01, pwrMessageESX02, uptimeMessage]
