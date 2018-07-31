#!/usr/bin/env python
 
# from urllib.parse import parse

import urllib.request
import urllib.parse


 
def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

def getInboxes(apikey):
    data =  urllib.parse.urlencode({'apikey': apikey})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/get_inboxes/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

def getMessages(apikey, inboxID):
    data =  urllib.parse.urlencode({'apikey': apikey, 'inbox_id' : inboxID})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/get_messages/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
 
# resp =  sendSMS('A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ', '919205257278',
#     'TXTLCL ', 'This is your message')

inboxes = getInboxes('A4mhT8jM+RY-ePSJWXB0P5pJuT5BzBBlVAumiqQiZJ')
print (inboxes)