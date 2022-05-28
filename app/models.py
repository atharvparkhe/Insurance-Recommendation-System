from django.db import models
from base.models import *

gender = (("male","male"),("female","female"))

class UserModel(BaseUser):
    otp = models.IntegerField(default=0)
    gender = models.CharField(choices=gender, max_length=7, default=gender[0], null=True, blank=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    smoking = models.BooleanField(null=True, blank=True)
    alcoholic = models.BooleanField(null=True, blank=True)
    def __str__(self):
        return self.name

class UserData(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user_data")
    ecg = models.FloatField(null=True, blank=True)
    glucose = models.IntegerField(null=True, blank=True)
    cardio = models.BooleanField(null=True, blank=True)
    def __str__(self):
        return self.user.name
