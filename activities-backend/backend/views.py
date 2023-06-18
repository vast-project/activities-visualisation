from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
#from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from backend.serializers import *
from activity_data.models import *
from django_filters.rest_framework import DjangoFilterBackend

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

class OrganisationTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows OrganisationTypes to be viewed or edited.
    """
    queryset = OrganisationType.objects.all()
    serializer_class = OrganisationTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class OrganisationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Organisation objects to be viewed or edited.
    """
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Event objects to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class ContextViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Context objects to be viewed or edited.
    """
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class NatureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Nature objects to be viewed or edited.
    """
    queryset = Nature.objects.all()
    serializer_class = NatureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class EducationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Education objects to be viewed or edited.
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Activity objects to be viewed or edited.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class StimulusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Stimulus objects to be viewed or edited.
    """
    queryset = Stimulus.objects.all()
    serializer_class = StimulusSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class ActivityStepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ActivityStep objects to be viewed or edited.
    """
    queryset = ActivityStep.objects.all()
    serializer_class = ActivityStepSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class AgeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Age objects to be viewed or edited.
    """
    queryset = Age.objects.all()
    serializer_class = AgeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class GenderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Gender objects to be viewed or edited.
    """
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class NationalityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Nationality objects to be viewed or edited.
    """
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Class objects to be viewed or edited.
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class VisitorGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows VisitorGroup objects to be viewed or edited.
    """
    queryset = VisitorGroup.objects.all()
    serializer_class = VisitorGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class VisitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Visitor objects to be viewed or edited.
    """
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class ProductTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ProductType objects to be viewed or edited.
    """
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Product objects to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class ConceptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Concept objects to be viewed or edited.
    """
    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class PredicateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Predicate objects to be viewed or edited.
    """
    queryset = Predicate.objects.all()
    serializer_class = PredicateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class StatementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Context objects to be viewed or edited.
    """
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = '__all__'

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
