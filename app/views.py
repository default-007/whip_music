from django.shortcuts import redirect, render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from app.models import *
from app.serializers import *
from app import settings
import math
import random
import requests

# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlanViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        auth_token = settings.FLW_SECRET_KEY
        url = "https://api.flutterwave.com/v3/payment-plans"

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + auth_token,
            "Content-Type": "application/json",
        }

        queryset = requests.request("GET", url, headers=headers)
        print(queryset.text)
        return Response(queryset.json())


class SubscriptionViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        auth_token = settings.FLW_SECRET_KEY
        url = "https://api.flutterwave.com/v3/transactions"
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + auth_token,
            "Content-Type": "application/json",
        }
        queryset = requests.request("GET", url, headers=headers)
        return Response(queryset.json())

    def create(self, request, *args, **kwargs):
        auth_token = settings.FLW_SECRET_KEY
        url = "https://api.flutterwave.com/v3/charges?type=mpesa"
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + auth_token,
            "Content-Type": "application/json",
        }
        planurl = "https://api.flutterwave.com/v3/payment-plans/16350"
        plan = requests.request("GET", planurl, headers=headers).json()
        print(plan)
        user = request.user
        payload = {
            "amount": plan["data"]["amount"],
            "currency": plan["data"]["currency"],
            "email": user.email,
            "tx_ref": "Mc" + str(math.floor(1000000 + random.random() * 9000000)),
            "phone_number": user.profile.phone_number,
            "fullname": user.first_name + "" + user.last_name,
            "preauthorize": False,
            "payment_plan": plan["data"]["id"],
        }
        res = requests.request("POST", url, json=payload, headers=headers)
        print(res)

        if res.status_code == 200:
            user.profile.is_premium = True
            user.profile.payment_status = "Paid"
        else:
            print("Error")
        return Response(res.json())
