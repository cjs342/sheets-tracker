"""
Receives and Responds to an SMS via Twilio.
Code taken from: https://www.twilio.com/docs/guides/how-to-receive-and-reply-in-python#generating-twiml-in-your-web-application
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from spreadsheet import writeToSpreadsheet, getLastEntry
import private

# message type codes
ENTRY = 1
LAST = 2
LIST = 3

categories = private.getCategories()
#columns = private.getColumns()

app = Flask(__name__)

@app.route('/sms', methods=['POST'])

def sms():
    number = request.form['From']
    message_body = request.form['Body']

    msg_type = getMessageType(message_body)
    #resp = MessagingResponse()
    #resp.message('{}'.format(msg_type))
    #return str(resp)


    valid,code = checkForErrors(message_body,categories,msg_type)

    resp = MessagingResponse()
    if valid:
        if msg_type == ENTRY:
            cat_key = message_body[0].lower()
            amount = getCharge(message_body)
            cat_name = categories[cat_key]
            resp.message('${} {} charge logged'.format(amount, cat_name))
            writeToSpreadsheet(cat_key, cat_name, amount)
        elif msg_type == LAST:
            last_cat, last_amt = getLastEntry()
            resp.message('Last entry: "${} {} charge logged"'.format(last_amt, last_cat))
        elif msg_type == LIST:
            keys = [x for x in categories]
            vals = [categories[x] for x in categories]
            lst = set(zip(keys,vals))
            resp.message('Categories: {}'.format(lst))

    else:
        resp.message('Error Code {}'.format(code))

    #resp.message('Hello {}, you said: {}'.format(number, message_body))

    #writeToSpreadsheet(1,1,message_body)

    return str(resp)

def getMessageType(message_body):
    if message_body.lower() == "list":
        return LIST
    elif message_body.lower() == "last":
        return LAST
    else:
        return ENTRY


def checkForErrors(s,categories,msg_type):
    if msg_type == ENTRY:
        if len(s) == 0:
            return False,1
        elif s[0].lower() not in categories:
            return False,2
        elif s[0].isdigit(): #or s[1].isdigit():
            return False,3
    elif msg_type == LAST:
        pass
    elif msg_type == LIST:
        pass

    return True,0

def getCharge(s):
    i1 = 0
    i2 = 0
    for i,c in enumerate(s):
        if c.isdigit():
            i1 = i
            break
    for i,c in enumerate(s[i1:]):
        if not c.isdigit():
            i2 = i+i1
            break
        i2 = len(s) - 1

    return s[i1:i2+1]



if __name__ == '__main__':
    app.run()
