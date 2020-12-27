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
    except ValueError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing configVersion field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if config['configVersion'] != '1.0.0':  # Validating whether or not this JSON has the proper version number.
        print('E: %s -- Validate JSON Thread -- JSON version mismatch...' % datetime.now())
        return False, None  # If version mismatch, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking API Key...' % datetime.now())
        value = config['apiKey']
        print('I: %s -- Validate JSON Thread -- API Key is %s characters long...' % datetime.now(), str(len(value)))
    except ValueError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing apiKey field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking ownerID...' % datetime.now())
        value = config['ownerID']
        print('I: %s -- Validate JSON Thread -- OwnerID is %s characters long...' % datetime.now(), str(len(value)))
    except ValueError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing ownerID field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - ownerID cannot be blank...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking announcementChannel...' % datetime.now())
        value = config['announcementChannel']
        print('I: %s -- Validate JSON Thread -- announcementChannel is %s characters long...' % datetime.now(), str(len(value)))
    except ValueError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing announcementChannel field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - announcementChannel cannot be blank...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.


    try:    # Validating whether or not this JSON has the proper fields.
        print('I: %s -- Validate JSON Thread -- Checking statusChannelWebhook...' % datetime.now())
        value = config['statusChannelWebhook']
        print('I: %s -- Validate JSON Thread -- statusChannelWebhook is %s characters long...' % datetime.now(), str(len(value)))
    except ValueError as err:
        print('E: %s -- Validate JSON Thread -- JSON invalid - Missing statusChannelWebhook field...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.

    if value == '':
        print('E: %s -- Validate JSON Thread -- JSON invalid - statusChannelWebhook cannot be blank...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.
    elif "https://discord.com/api/webhooks/" not in value:
        print('E: %s -- Validate JSON Thread -- JSON invalid - statusChannelWebhook must contain "https://discord.com/api/webhooks/"...' % datetime.now())
        return False, None  # If there is an error JSON is invalid, return False and no data.



