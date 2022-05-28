from rest_framework import serializers
from .models import *


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)


class signupSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)


class otpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required = True)
    pw = serializers.CharField(required = False)


class emailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)


class healthSerializer(serializers.Serializer):
    height = serializers.FloatField(required = True)
    weight = serializers.FloatField(required = True)
    smoking = serializers.BooleanField(required = True)
    alcoholic = serializers.BooleanField(required = True)
    dob = serializers.DateField(required = True)
    gender = serializers.CharField(required = True)


class UserDataSerializer(serializers.Serializer):
    ecg = serializers.BooleanField(required = True)
    bps = serializers.IntegerField(required = True)
    bpd = serializers.IntegerField(required = True)
    cardio = serializers.BooleanField(required = True)
