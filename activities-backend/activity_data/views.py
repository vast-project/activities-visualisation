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

from django.contrib.auth.models import User
from django.db import models
from .models import Age
from .models import Gender
from .models import Education
from .models import Nationality
from .models import Language
from .models import Activity
from .models import VisitorGroup

from .utils import VASTRepositoryAPIView

class ProductView(VASTRepositoryAPIView):

    # Create a new instance. (POST)
    def create(self, request):
        activity_step = self.request_data(request, "activity_step")

@api_view(['POST'])
@csrf_exempt
def saveproduct(request):
    if request.method=='POST':
        if request.data['activity_step'] is not None:
            alldata = VisitorGroup.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata=alldata.filter(name=request.data['activity_step'])
                for dat in userdata:
                    request.data['activity_step']=dat.id
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
        if request.data['age'] is not None:
            alldata = Age.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata=alldata.filter(name=request.data['age'])
                for dat in userdata:
                    request.data['age']=dat.id
        if request.data['gender'] is not None:
            alldata = Gender.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata=alldata.filter(name=request.data['gender'])
                for dat in userdata:
                    request.data['gender']=dat.id
        if request.data['education'] is not None:
            alldata = Education.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata=alldata.filter(name=request.data['education'])
                for dat in userdata:
                    request.data['education']=dat.id
        if request.data['nationality'] is not None:
            alldata = Nationality.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata=alldata.filter(name=request.data['nationality'])
                for dat in userdata:
                    request.data['nationality']=dat.id
        if request.data['motherLanguage'] is not None:
            alldata = Language.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata=alldata.filter(name=request.data['motherLanguage'])
                for dat in userdata:
                    request.data['motherLanguage']=dat.id
        if request.data['group'] != 0:
            alldata = VisitorGroup.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata=alldata.filter(name=request.data['group'])
                for dat in userdata:
                    request.data['group']=dat.id
        else:
            request.data['group'] = 1
        if request.data['activity'] == 0:
            request.data['activity'] = 1
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


