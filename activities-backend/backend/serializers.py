from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from activity_data.models import *

class UserSerializerURL(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url']

class AutoUserModelSerializer(serializers.Serializer):
    # created_by = serializers.HiddenField( 
    #     default=serializers.CurrentUserDefault()
    # )
    # created_by = serializers.PrimaryKeyRelatedField(
    #         read_only=True,
    #         default=serializers.CreateOnlyDefault(CurrentUserDefault())
    # )
    # https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/#hyperlinking-our-api
    # Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField
    created_by = serializers.HyperlinkedRelatedField(
            view_name="user-detail",
            read_only=True, 
            default=CurrentUserDefault()
    )
    def save(self, **kwargs):
        if self.instance is None:
            """Include default for read_only `created_by` field"""
            kwargs["created_by"] = self.fields["created_by"].get_default()
        return super().save(**kwargs)

class LanguageSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class OrganisationTypeSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = OrganisationType
        fields = '__all__'

class OrganisationSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class EventSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ContextSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Context
        fields = '__all__'

class NatureSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Nature
        fields = '__all__'

class EducationSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class ActivitySerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class StimulusSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Stimulus
        fields = '__all__'

class ActivityStepSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = ActivityStep
        fields = '__all__'

class AgeSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Age
        fields = '__all__'

class GenderSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class NationalitySerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'

class ClassSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class VisitorGroupSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = VisitorGroup
        fields = '__all__'

class VisitorSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

class ProductTypeSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ConceptSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Concept
        fields = '__all__' 

class PredicateSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Predicate
        fields = '__all__' 
  
class StatementSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = Statement
        fields = '__all__' 
          
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
