import pickle

from config import config

TW_SID = config["tw_sid"]
TW_TOKEN = config["tw_token"]
TW_NUMBER = config["tw_number"]
NUMBERS = config["numbers"]

from twilio.rest import Client
tw = Client(TW_SID, TW_TOKEN)

def alert(message):
    '''
    Helper method to send an alert via SMS or email
    listing: dictionary of availability date and price of listing
    message: string, either "added" or "removed" to tell if the listing was added or removed
    '''
    for number in NUMBERS:
        tw.messages.create( 
            body = message,
            from_ = TW_NUMBER,
            to = number
        )

def get_messages():
    '''
    Gets all messages in the database
    '''
    for sms in tw.messages.list():
        print(sms)

if __name__ == "__main__":
    get_messages()
