from django.core.mail import EmailMessage
from django.conf import settings
from . models import User
import pyotp
from datetime import datetime, timedelta
import random


#creating the otp
def generate_otp():
    otp=""
    for i in range(6):
        otp  += str(random.randint(0,9))
    return otp

def email_sender(email):
    subject = 'One Time Password'
    user = User.objects.get(email=email)
    otp = generate_otp()
    print(otp)
    body = f'Hello {user.first_name}, \nYour One Time Password is {otp} \nNote that the OTP Expires after 2 minutes'
    email_from = settings.DEFAULT_FROM_EMAIL

    user.email_otp = otp
    user.save()

    send_email = EmailMessage(subject=subject,body=body,from_email=email_from,to=[email])
    send_email.send(fail_silently=True)



