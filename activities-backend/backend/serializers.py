from django.contrib.auth.models import User, Group
from rest_framework import serializers

from activity_data.models import *

class OrganisationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganisationType
        fields = '__all__'

class ClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class StimulusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stimulus
        fields = '__all__'

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ContextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Context
        fields = '__all__'

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class AgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Age
        fields = '__all__'

class GenderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class EducationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class NationalitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'

class NatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nature
        fields = '__all__'

class ActivityStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityStep
        fields = '__all__'

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class VisitorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

class VisitorGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VisitorGroup
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
