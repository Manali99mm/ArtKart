import random
import smtplib, ssl
import os
from email.mime.text import MIMEText

class User:
    userSchema = {
        'bsonType': 'object',
        'additionalProperties': True,
        'required': ['email', 'password', 'location', 'is_artist'],
        'properties': {
            'name': {
                'bsonType': 'string',
            },
            'email': {
                'bsonType': 'string'
            },
            'password': {
                'bsonType': 'string',
                'minimum': 8,
                'maximum': 255
            },
            'profile_pic': {
                'bsonType': 'string'
            },
            'bio': {
                'bsonType': 'string'
            },
            'is_artist': {
                'type': 'boolean',
                # 'default': False
            },
            'location': {
                'bsonType': 'object',
                'required': ['city', 'state', 'country'],
                'properties': {
                    'city': {
                        'bsonType': 'string'
                    },
                    'state': {
                        'bsonType': 'string'
                    },
                    'country': {
                        'bsonType': 'string'
                    }
                }
            }
        }
    }

    def generateOTP(otp_size = 6):
        final_otp = ''
        for i in range(otp_size):
            final_otp = final_otp + str(random.randint(0,9))
        return final_otp

    def sendEmailVerificationRequest(receiver, sender=os.environ.get('SENDER_MAIL'), subject="OTP Verification"):
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
        server.login(sender, os.environ.get('GOOGLE_APP_PASSWORD'))
        cur_otp = User.generateOTP()
        msg = """Hello,\nPlease use the OTP verification code below on the ArtKart app\n\n%s\n\nThanks,\nArtKart Team""" % (cur_otp)
        message = MIMEText(msg)
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = receiver
        server.sendmail(sender, receiver, message.as_string())
        server.quit()
        return cur_otp