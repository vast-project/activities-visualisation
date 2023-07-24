from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from activity_data.serialize import Productserialize
from activity_data.serialize import Visitorserialize
from .models import Age, ProductType, Visitor, ActivityStep, Product
from .models import Education
from .models import Gender
from .models import Language
from .models import Nationality
from .models import VisitorGroup
from .utils import VASTRepositoryAPIView


class ProductView(VASTRepositoryAPIView):
    # Create a new instance. (POST)
    def create(self, request):
        activity_step = self.request_data(request, "activity_step")


@api_view(['POST'])
@csrf_exempt
def saveproduct(request):
    if request.method == 'POST':
        if request.data['activity_step'] is not None:
            alldata = VisitorGroup.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata = alldata.filter(name=request.data['activity_step'])
                for dat in userdata:
                    request.data['activity_step'] = dat.id
        saveserialize = Productserialize(data=request.data)
        if saveserialize.is_valid():
            saveserialize.save()
            return Response(saveserialize.data, status=status.HTTP_201_CREATED)
        else:
            return Response(saveserialize.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def save_statements(request):
    data = request.data

    # Find user to use as created_by (based on the given username)
    creator_user = User.objects.get(username=data["creator_username"])
    if not creator_user:
        return Response({"error": "Error saving statement"}, status=status.HTTP_400_BAD_REQUEST)

    # Find visitor
    visitor_name = data["visitor_name"]
    visitor = Visitor.objects.get(name=visitor_name, created_by=creator_user)

    # Find product type, or create it
    product_type_name = data["product"]
    product_type, _ = ProductType.objects.get_or_create(name=product_type_name, created_by=creator_user)

    # Find activity step
    activity_step = ActivityStep.objects.get(id=data["activity_step"])

    # Get or create the product in the DB
    product_name = "-".join([visitor_name, product_type_name, activity_step.name])
    product, _ = Product.objects.get_or_create(name=product_name, created_by=creator_user, product_type_id=product_type.id,
                                            activity_step_id=activity_step.id, visitor_id=visitor.id)

    # todo: Get or create a subject in the DB (based on the given one, and its language)

    # todo: For each predicate:
    #           - Check if it exists in the DB, if not, create it
    #           - Create the statements, by creating new objects for each array element, connecting them with the
    #               subject via the predicate

    return Response({"hello": True}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@csrf_exempt
def savevisitor(request):
    if request.method == 'POST':
        if request.data['age'] is not None:
            alldata = Age.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata = alldata.filter(name=request.data['age'])
                for dat in userdata:
                    request.data['age'] = dat.id
        if request.data['gender'] is not None:
            alldata = Gender.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata = alldata.filter(name=request.data['gender'])
                for dat in userdata:
                    request.data['gender'] = dat.id
        if request.data['education'] is not None:
            alldata = Education.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata = alldata.filter(name=request.data['education'])
                for dat in userdata:
                    request.data['education'] = dat.id
        if request.data['nationality'] is not None:
            alldata = Nationality.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata = alldata.filter(name=request.data['nationality'])
                for dat in userdata:
                    request.data['nationality'] = dat.id
        if request.data['motherLanguage'] is not None:
            alldata = Language.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata = alldata.filter(name=request.data['motherLanguage'])
                for dat in userdata:
                    request.data['motherLanguage'] = dat.id
        if request.data['group'] != 0:
            alldata = VisitorGroup.objects.all()
            qslist = []
            users = User.objects.filter(groups__name="Museo Galileo")
            for user in users:
                userdata = alldata.filter(name=request.data['group'])
                for dat in userdata:
                    request.data['group'] = dat.id
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
        return Response({'message': "ok: get"})

    def post(self, request, format=None):
        print("++++++++++++++++++++++++++++++++++++++")
        for k, v in request.data.items():
            print(f"  {k}={v}")
        return Response({'message': "ok: post"})
