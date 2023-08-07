from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.response import Response

from backend.serializers import *
from allauth.socialaccount.models import *


class FilteringModelViewSet(viewsets.ModelViewSet):
    filterset_fields = '__all__'
    # @action(methods=['GET'], detail=False)
    # def filter(self, request): 
    #     queryset = self.get_queryset()
    #     filtered_queryset = self.filter_queryset(queryset)
    #     serializer = self.serializer_class(filtered_queryset, context={'request': request}, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class LanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Language objects to be viewed or edited.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name', 'code']


class OrganisationTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows OrganisationTypes to be viewed or edited.
    """
    queryset = OrganisationType.objects.all()
    serializer_class = OrganisationTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class OrganisationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Organisation objects to be viewed or edited.
    """
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Event objects to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class ContextViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Context objects to be viewed or edited.
    """
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class NatureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Nature objects to be viewed or edited.
    """
    queryset = Nature.objects.all()
    serializer_class = NatureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class EducationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Education objects to be viewed or edited.
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Activity objects to be viewed or edited.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class StimulusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Stimulus objects to be viewed or edited.
    """
    queryset = Stimulus.objects.all()
    serializer_class = StimulusSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class ActivityStepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ActivityStep objects to be viewed or edited.
    """
    queryset = ActivityStep.objects.all()
    serializer_class = ActivityStepSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class AgeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Age objects to be viewed or edited.
    """
    queryset = Age.objects.all()
    serializer_class = AgeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class GenderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Gender objects to be viewed or edited.
    """
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class NationalityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Nationality objects to be viewed or edited.
    """
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Class objects to be viewed or edited.
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class VisitorGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows VisitorGroup objects to be viewed or edited.
    """
    queryset = VisitorGroup.objects.all()
    serializer_class = VisitorGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class VisitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Visitor objects to be viewed or edited.
    """

    # def get_permissions(self):
    #     """Returns the permission based on the type of action"""

    #     if self.action == "create":
    #         # allow anyone to create a visitor, so that visitors won't have to
    #         # authenticate to the API to use the app.
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]

    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    filterset_fields = '__all__'
    search_fields = ['name']

    # def create(self, request, *args, **kwargs):
    #     # Find user by the username in the POST body, and set it as the user of the request
    #     creator_user = User.objects.get(username=request.data['creator_username'])
    #     if creator_user is not None:
    #         # We could do "request.user = creator_user" and return super().create(request, *args, **kwargs) if we could create hyperlinks from the parameters.
    #         # Instead, we create the object manually and return it.
    #         new_visitor = Visitor()

    #         new_visitor.created_by = creator_user
    #         new_visitor.name = request.data['name']
    #         new_visitor.school = request.data['school']
    #         new_visitor.date_of_visit = request.data['date_of_visit']

    #         new_visitor.activity_id = int(request.data['activity'])
    #         new_visitor.activity_step_id = int(request.data['activity_step'])
    #         new_visitor.visitor_group = VisitorGroup.objects.filter(id=int(request.data['visitor_group'])).first()

    #         new_visitor.age = Age.objects.filter(name=request.data['age']).first()
    #         new_visitor.gender = Gender.objects.filter(name=request.data['gender']).first()
    #         new_visitor.nationality = Nationality.objects.filter(name=request.data['nationality']).first()
    #         new_visitor.education = Education.objects.filter(name=request.data['education_level']).first()
    #         new_visitor.mother_language = Language.objects.filter(name=request.data['mother_language']).first()

    #         new_visitor.save()
    #         return Response(VisitorSerializer(new_visitor, context={"request": request}).data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ProductType objects to be viewed or edited.
    """
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Product objects to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class ConceptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Concept objects to be viewed or edited.
    """
    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class PredicateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Predicate objects to be viewed or edited.
    """
    queryset = Predicate.objects.all()
    serializer_class = PredicateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class StatementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Context objects to be viewed or edited.
    """
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class DigitisationApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Context objects to be viewed or edited.
    """
    queryset = DigitisationApplication.objects.all()
    serializer_class = DigitisationApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']


class VisitorGroupQRCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Context objects to be viewed or edited.
    """
    queryset = VisitorGroupQRCode.objects.all()
    serializer_class = VisitorGroupQRCodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filterset_fields = '__all__'
    filterset_fields = ['name', 'description', 'name_local', 'description_local',
                        'event', 'activity', 'activity_step', 'visitor_group', 'application']
    search_fields = ['name']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['username','email']


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']
