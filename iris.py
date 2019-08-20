import pickle
import datetime
import os.path

from config import config, rules

TW_SID = config["tw_sid"]
TW_TOKEN = config["tw_token"]
TW_NUMBER = config["tw_number"]

from twilio.rest import Client
tw = Client(TW_SID, TW_TOKEN)

#def load_receipts(rules)
#    '''
#    Set up receipts, which record whether a rule has
#    been responded to
#    '''
#    if os.path.isfile('receipt.p'):
#        return pickle.load(open('receipt.p', 'rb'))
#    else:
#        return [False for rule in rules]


def alert(nuber, message):
    '''
    Helper method to send an alert via SMS or email
    listing: dictionary of availability date and price of listing
    message: string, either "added" or "removed" to tell if the listing was added or removed
    '''
    tw.messages.create( 
        body = message,
        from_ = TW_NUMBER,
        to = number
    )

def get_messages(sender):
    '''
    Gets all incoming messages in the database
    sender: the origin number SMS is delivered from
    '''
    messages = []
    today = datetime.datetime.now()
    for sms in tw.messages.list(limit=5, from_=sender, date_sent_after = datetime.datetime(today.year, today.month, today.day + 1, 0,0), date_sent_before = datetime.datetime(today.year, today.month, today.day + 1, 12, 0)):
        print(sms.date_sent)
        messages.append(sms)
    return messages
        
if __name__ == "__main__":
    for rule in rules:
        numbers = rule['numbers']
        for number in numbers:
            messages = get_messages(number)
            if len(messages) < 1:
                print('alerting')
                alert(number, rule['message'])
