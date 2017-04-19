import time
import requests
import json
import smtplib

sender = 'klaas.denys@outlook.com'
receivers = ['klaas.denys@outlook.com']
message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

a=0
while 1:
    r = requests.get("http://www.dhl.be/shipmentTracking?AWB=3338444303&countryCode=be&languageCode=en&_=1492515415508")
    object = json.loads(r.content, object_hook=AttrDict)
    # print (r.content)
    #print(object.results[0].checkpoints)
    if len( object.results[0].checkpoints)>a:
        print (object.results[0].checkpoints[0].counter)
        try:
            smtpObj = smtplib.SMTP('012.net.il')
            smtpObj.sendmail(sender, receivers, message)
            smtpObj.quit()
            print "Successfully sent email"
        except smtplib.SMTPException:
            print "Error: unable to send email"
        a=a+1
    time.sleep(5)
