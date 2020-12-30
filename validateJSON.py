import json
from datetime import datetime


def validateJSON(jsonFile):

    try:    # Validating whether or not this is a valid JSON file.
        print('I: %s -- Validate JSON Thread -- Validating config file...' % datetime.now())  # Print console log
        config = json.load(jsonFile)
    except ValueError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid exiting...' % datetime.now())
        return False, None


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking config file version...' % datetime.now())
        print('I: %s -- Validate JSON Thread -- Config file version is: ' % datetime.now(), config['configVersion'] )
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing configVersion field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if config['configVersion'] != '1.0.0':  # Validating whether or not this JSON has the proper version number.
        print('E: %s -- Validate JSON Thread -- JSON version mismatch...' % datetime.now())
        return False, None  # If version mismatch, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking API Key...' % datetime.now())
        value = config['apiKey']
        print('I: %s -- Validate JSON Thread -- API Key field exists...' % datetime.now())
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing apiKey field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking ownerID...' % datetime.now())
        value = config['ownerID']
        print('I: %s -- Validate JSON Thread -- OwnerID field exists...' % datetime.now())
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing ownerID field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - ownerID cannot be blank...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking commandPrefix...' % datetime.now())
        value = config['commandPrefix']
        print('I: %s -- Validate JSON Thread -- commandPrefix field exists...' % datetime.now())
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing commandPrefix field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - commandPrefix cannot be blank...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking announcementChannelID...' % datetime.now())
        value = config['announcementChannelID']
        print('I: %s -- Validate JSON Thread -- announcementChannelID field exists...' % datetime.now())
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing announcementChannelID field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - announcementChannel cannot be blank...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking statusChannelWebhook...' % datetime.now())
        value = config['statusChannelWebhook']
        print('I: %s -- Validate JSON Thread -- statusChannelWebhook field exists...' % datetime.now())
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing statusChannelWebhook field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - statusChannelWebhook cannot be blank...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.
    elif "https://discord.com/api/webhooks/" not in value:
        print('E: %s -- Validate JSON Thread -- JSON invalid - statusChannelWebhook must contain "https://discord.com/api/webhooks/"...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking gameName...' % datetime.now())
        value = config['gameName']
        print('I: %s -- Validate JSON Thread -- gameName is %s...' % (datetime.now(), value))
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing gameName field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        config['gameName'] = None


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking dbUser...' % datetime.now())
        value = config['dbUser']
        print('I: %s -- Validate JSON Thread -- dbUser field exists...' % datetime.now())
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing dbUser field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - dbUser field cannot be empty...' % datetime.now())
        return False, None


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking dbUserPassword...' % datetime.now())
        value = config['dbPassword']
        print('I: %s -- Validate JSON Thread -- dbPassword field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing dbPassword field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - dbPassword field cannot be empty...' % datetime.now())
        return False, None


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking dbHost...' % datetime.now())
        value = config['dbHost']
        print('I: %s -- Validate JSON Thread -- dbHost field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing dbHost field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - dbHost field cannot be empty...' % datetime.now())
        return False, None


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking dbPort...' % datetime.now())
        value = config['dbPort']
        print('I: %s -- Validate JSON Thread -- dbPort field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing dbPort field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - dbPort field cannot be empty...' % datetime.now())
        return False, None


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking vmwareStatsDB...' % datetime.now())
        value = config['vmwareStatsDB']
        print('I: %s -- Validate JSON Thread -- vmwareStatsDB field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing vmwareStatsDB field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        config['vmwareStatsDB'] = None


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking notificationDB...' % datetime.now())
        value = config['notificationDB']
        print('I: %s -- Validate JSON Thread -- notificationDB field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing notificationDB field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        config['notificationDB'] = None


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking dbSeries...' % datetime.now())
        value = config['dbSeries']
        print('I: %s -- Validate JSON Thread -- dbSeries field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing dbSeries field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        config['dbSeries'] = None


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking pollingRate...' % datetime.now())
        value = config['pollingRate']
        print('I: %s -- Validate JSON Thread -- pollingRate field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing pollingRate field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        config['pollingRate'] = '60'


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking truenasNotifyDB...' % datetime.now())
        value = config['speedTestDB']
        print('I: %s -- Validate JSON Thread -- speedTestDB field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing speedTestDB field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        config['speedTestDB'] = None


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking mention...' % datetime.now())
        value = config['mention']
        print('I: %s -- Validate JSON Thread -- mention field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing mention field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:  # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking debug...' % datetime.now())
        value = config['debug']
        print('I: %s -- Validate JSON Thread -- debug field exists...' % datetime.now(), value)
    except KeyError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing debug field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    return True, config
