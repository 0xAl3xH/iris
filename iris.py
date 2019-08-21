import pickle
import time
import pendulum as pd
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


def alert(number, message):
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

def get_messages(sender, start, end):
    '''
    Gets all incoming messages in the database
    sender: the origin number SMS is delivered from
    '''
    messages = []
    smses = tw.messages.list(limit=5, from_=sender, date_sent_after = start, date_sent_before = end)
    print('Found', len(smses), 'mesages, sent on:')
    for sms in smses:
        print(sms.date_sent)
        messages.append(sms)
    return messages

def run_rule(rule):
    now = pd.now().add(days=1)
    start_time, end_time = rule['start_time'], rule['end_time']
    # TODO: figure out if these times need to be in UTC time zone
    start = now.replace(hour = start_time.hour, minute = start_time.minute, second = start_time.second).in_timezone('UTC')
    end = now.replace(hour = end_time.hour, minute = end_time.minute, second = end_time.second).in_timezone('UTC')
    numbers = rule['numbers']
    message = rule['message']
    delay = rule['delay']
    delay_count = rule.setdefault('delay_count', 0)

    if delay_count == 0:
        rule['delay_count'] = (now - start).in_minutes() // delay + 1

    print(delay_count, now, start.add(minutes=delay_count * delay).in_timezone('America/Los_Angeles'))

    if now >= start.add(minutes=delay_count * delay).in_timezone('America/Los_Angeles') and now <= end:
        print(delay_count, now, start.add(minutes=delay_count * delay).in_timezone('America/Los_Angeles'))
        for number in numbers:
            messages = get_messages(number, start, end)
            if len(messages) < 1:
                print('Alerting', number, 'with message:', message)
                rule['delay_count'] = rule['delay_count'] + 1
                print(rule)
                alert(number, message)
            else:
                # TODO: apply a timestamp so we can skip checking messages that already have a response 
                rule['delay_count'] = 0
        
if __name__ == "__main__":
    while True:
        for rule in rules:
            run_rule(rule)
        time.sleep(10)
