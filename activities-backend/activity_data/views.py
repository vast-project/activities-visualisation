from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
    
class StoreActivityData(APIView):
    def get(self, request, format=None):
        print("======================================")
        print(request)
        return Response({'message':"ok: get"})

    def post(self, request, format=None):
        print("++++++++++++++++++++++++++++++++++++++")
        for k,v in request.data.items():
            print(f"  {k}={v}")
        return Response({'message':"ok: post"})

