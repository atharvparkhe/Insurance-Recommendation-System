import threading, random
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

class ForgotEmail(threading.Thread):
    def __init__(self, user_obj):
        self.user_obj = user_obj
        threading.Thread.__init__(self)
    def run(self):
        try:
            otp = random.randint(100001, 999999)
            self.user_obj.otp = otp
            self.user_obj.save()
            subject = "Change Password Request"
            message = f"The OTP to change your password is {otp} \nIts valid only for 2 mins."
            email_from = settings.EMAIL_HOST_USER
            print("email sending")
            send_mail(subject , message ,email_from ,[self.user_obj.email])
            print("email sending")
        except Exception as e:
            print(e)