from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from activity_data.models import Product
from activity_data.serialize import Productserialize
from activity_data.models import Visitor
from activity_data.serialize import Visitorserialize
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@csrf_exempt
def saveproduct(request):
    if request.method=='POST':
        saveserialize = Productserialize(data=request.data)
        if saveserialize.is_valid():
            saveserialize.save()
            return Response(saveserialize.data, status=status.HTTP_201_CREATED)
        else:
            return Response(saveserialize.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def savevisitor(request):
    if request.method=='POST':
        saveserialize = Visitorserialize(data=request.data)
        if saveserialize.is_valid():
            saveserialize.save()
            return Response(saveserialize.data, status=status.HTTP_201_CREATED)
        else:
            return Response(saveserialize.data, status=status.HTTP_400_BAD_REQUEST)
        
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


