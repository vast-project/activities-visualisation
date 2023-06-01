from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from backend.serializers import *
from activity_data.models import *

class OrganisationTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows OrganisationTypes to be viewed or edited.
    """
    queryset = OrganisationType.objects.all()
    serializer_class = OrganisationTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Class objects to be viewed or edited.
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrganisationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Organisation objects to be viewed or edited.
    """
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Event objects to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

class StimulusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Stimulus objects to be viewed or edited.
    """
    queryset = Stimulus.objects.all()
    serializer_class = StimulusSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Product objects to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContextViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Context objects to be viewed or edited.
    """
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]

class LanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Language objects to be viewed or edited.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

class AgeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Age objects to be viewed or edited.
    """
    queryset = Age.objects.all()
    serializer_class = AgeSerializer
    permission_classes = [permissions.IsAuthenticated]

class GenderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Gender objects to be viewed or edited.
    """
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [permissions.IsAuthenticated]

class EducationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Education objects to be viewed or edited.
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

class NationalityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Nationality objects to be viewed or edited.
    """
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [permissions.IsAuthenticated]

class NatureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Nature objects to be viewed or edited.
    """
    queryset = Nature.objects.all()
    serializer_class = NatureSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActivityStepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ActivityStep objects to be viewed or edited.
    """
    queryset = ActivityStep.objects.all()
    serializer_class = ActivityStepSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Activity objects to be viewed or edited.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

class VisitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Visitor objects to be viewed or edited.
    """
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [permissions.IsAuthenticated]

class VisitorGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows VisitorGroup objects to be viewed or edited.
    """
    queryset = VisitorGroup.objects.all()
    serializer_class = VisitorGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

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
