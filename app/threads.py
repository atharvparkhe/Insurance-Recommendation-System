import threading, random
from django.conf import settings
from django.core.mail import send_mail
from models.cardio import useCardio
from models.ecg import useECG
from models.glucose import useGlucose

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



class GlucoseDataThread(threading.Thread):
    def __init__(self, user_data):
        self.user_data = user_data
        threading.Thread.__init__(self)
    def run(self):
        try:
            self.user_data.glucose = useGlucose()
            self.save()
        except Exception as e:
            print(e)


class CardioDataThread(threading.Thread):
    def __init__(self, user_data):
        self.user_data = user_data
        threading.Thread.__init__(self)
    def run(self):
        try:
            self.user_data.cardio = useGlucose()
            self.save()
        except Exception as e:
            print(e)


class ECGDataThread(threading.Thread):
    def __init__(self, user_data):
        self.user_data = user_data
        threading.Thread.__init__(self)
    def run(self):
        try:
            self.user_data.ecg = useGlucose()
            self.save()
        except Exception as e:
            print(e)

