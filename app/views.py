from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from threading import Thread
from .serializers import *
from .threads import *
from .models import *


@api_view(["POST"])
def signUp(request):
    try:
        data = request.data
        serializer = signupSerializer(data=data)
        if serializer.is_valid():
            name = serializer.data["name"]
            email = serializer.data["email"]
            password = serializer.data["password"]
            if UserModel.objects.filter(email=email).first():
                return Response({"message":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_customer = UserModel.objects.create(email=email, name=name)
            new_customer.set_password(password)
            new_customer.save()
            return Response({"message":"Account created"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def logIn(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            customer_obj = UserModel.objects.filter(email=email).first()
            if customer_obj is None:
                return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=password)
            if not user:
                return Response({"message":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            return Response({"message":"Login successfull", "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def forgot(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            user_obj = UserModel.objects.filter(email=email).first()
            if not user_obj:
                return Response({"message":"User does not exist."}, status=status.HTTP_404_NOT_FOUND)
            thread_obj = ForgotEmail(user_obj)
            thread_obj.start()
            return Response({"message":"reset mail sent"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def reset(request):
    try:
        data = request.data
        serializer = otpSerializer(data=data)
        if serializer.is_valid():
            otp = serializer.data["otp"]
            if not UserModel.objects.filter(otp=otp):
                return Response({"message":"Invalid OTP"}, status=status.HTTP_404_NOT_FOUND)
            user_obj = UserModel.objects.get(otp=otp)
            user_obj.set_password(serializer.data["pw"])
            user_obj.otp = 0
            user_obj.save()
            return Response({"message":"Password changed successfull"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def health(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        data = request.data
        user = UserModel.objects.get(email=request.user.email)
        ser = healthSerializer(data=data)
        if ser.is_valid():
            user.height = ser.data["height"]
            user.weight = ser.data["weight"]
            user.smoking = ser.data["smoking"]
            user.alcoholic = ser.data["alcoholic"]
            user.dob = ser.data["dob"]
            user.gender = ser.data["gender"]
            user.save()
            return Response({"message":"user data saved"}, status=status.HTTP_200_OK)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def getData(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        user = UserModel.objects.get(email=request.user.email)
        ser = UserDataSerializer(data=request.data)
        abc, _ = UserData.objects.get_or_create(user=user)
        if ser.is_valid():
            abc.ecg = ser.data["ecg"]
            abc.bps = ser.data["bps"]
            abc.bpd = ser.data["bpd"]
            abc.cardio = ser.data["cardio"]
            abc.save()
            return Response({"message":"user data saved"}, status=status.HTTP_200_OK)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def checkData(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        user = UserModel.objects.get(email=request.user.email)
        if not user.height:
            return Response({"Has Filled":False}, status=status.HTTP_200_OK)
        else:return Response({"Has Filled":True}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def analyseData(request):
    try:
        context = {}
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        user_data_obj = UserData.objects.get(user=UserModel.objects.get(email=request.user.email))
        thread_obj_1 = GlucoseDataThread(user_data_obj)
        thread_obj_1.start()
        thread_obj_2 = CardioDataThread(user_data_obj)
        thread_obj_2.start()
        thread_obj_3 = ECGDataThread(user_data_obj)
        thread_obj_3.start()
        return Response({"messgae":"context"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def fetchResults(request):
    try:
        context = {}
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        user = UserModel.objects.get(email=request.user.email)
        user_data_obj = UserData.objects.get(user=user)
        if (not user_data_obj.ecg) or (not user_data_obj.glucose) or (user_data_obj.cardio):
            return Response({"message":"Values not yet updated. Try again later"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        context["ecg"] = user_data_obj.ecg
        context["glucose"] = user_data_obj.glucose
        context["cardio"] = user_data_obj.cardio
        context["gender"] = user.gender
        context["dob"] = user.dob
        context["height"] = user.height
        context["weight"] = user.weight
        context["smoking"] = user.smoking
        context["alcoholic"] = user.alcoholic
        return Response({"message":context}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)