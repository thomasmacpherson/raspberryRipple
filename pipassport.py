'''
Provides easy use of NFC card for Pi Passport to record data / attendance
at events etc.

Copyright (C) Open LX SP Ltd 2015 Andrew Robinson
                                  Thomas MacPherson Pope
                                  Amy Mather
                                  Thomas Preston

Contact: support@openlx.org.uk
'''
import json
import nxppy
import requests


DEFAULT_SERVER = 'api.pi-passport.net'
CARD_TYPE = 'mifare'


def get_card_id():
    '''Checks the NXP nfc card reader for a card identity'''
    mifare = nxppy.Mifare()
    while True:
        try:
            cardid = mifare.select()
            if cardid is not None:
                return cardid
        except nxppy.SelectError:
            pass


def request_user_info(apikey, cardid, server=DEFAULT_SERVER):
    '''Returns info about the user in a dictionary:
{
 'first_name' : '..........', --> returns the card holder's first name
 'last_name'  : '..........', --> returns the card holder's last name
 'success'    : True / False, --> returns whether or not the request was a success
 'card_status': '..........', --> returns if the card is active, retired or lost etc.
 'image_url'  : '..........', --> returns the url for an image of the card user
 'message'    : '..........'  --> returns the reason, if a request fails, why it has failed
                                  e.g. the card isn't registered in the database
}
'''
    url = ('http://{server}/transactions/user/?apikey={apikey}&'
           'cardid={cardid}&cardtype={cardtype}')
    return requests.get(url.format(server=server,
                                   apikey=apikey,
                                   cardid=cardid,
                                   cardtype=CARD_TYPE)).json


def card_valid(data):
    '''Checks the success message from the data returned by
    'request_user_info()' and returns a boolean response.
    '''
    return data['success'] and data['card_status'] == 'active'


def post_transaction(apikey, cardid, data, server=DEFAULT_SERVER):
    ''' Submits data to the database under the user's card ID for your
    application.

    Example uses:

        - to submit the user's scores from a game for a leaderboard
        - to indicate that the user has visited an event
        - to indicate that the user has borrowed a book
        - to save urls to images / videos of or by the user

    '''
    url = ('http://{server}/transactions/{apikey}/add/'
           'cardtype/{cardtype}/cardid/{cardid}/')
    return requests.post(url.format(server=server,
                                    apikey=apikey,
                                    cardtype=CARD_TYPE,
                                    cardid=cardid), data={'data': data}).json
