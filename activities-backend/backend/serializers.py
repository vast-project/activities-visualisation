from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from activity_data.models import *
from home.models import *
from allauth.socialaccount.models import *

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
            
        request = self.context.get("request")
        if request.user.is_authenticated:
            kwargs["created_by"] = request.user
        elif  request.user.is_anonymous: # AnonymousUser code
            kwargs["created_by"] = None
            # Get created_by value from the POST request
            created_by_id = request.data.get('created_by', User.objects.get(username='default_user').id)
            kwargs["created_by"] = User.objects.get(id=created_by_id)
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
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if not 'name' in data or not data['name']:
            data['name'] = ".".join([data['product_type'].name, str(data['visitor'].id), data['activity_step'].name])
        return data

    def create(self, validated_data):
        try:
            # if there is already an instance in the database with the
            # given value (e.g. tag='apple'), we simply return this instance
            return Product.objects.get(name=validated_data['name'])
        except ObjectDoesNotExist:
            return super().create(validated_data)

    class Meta:
        model = Product
        fields = '__all__'
        validators = [
        ]
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=model.objects.all(),
        #         fields=['name', 'created_by'],
        #        # message='Your custom message'
        #     )
        # ]


class ConceptTypeSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = ConceptType
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
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if not 'name' in data or not data['name']:
            data['name'] = ".".join([data['product'].name, data['subject'].name, data['predicate'].name, data['object'].name])
        return data

    def create(self, validated_data):
        try:
            # if there is already an instance in the database with the
            # given value (e.g. tag='apple'), we simply return this instance
            return Statement.objects.get(name=validated_data['name'])
        except ObjectDoesNotExist:
            return super().create(validated_data)

    class Meta:
        model = Statement
        fields = '__all__'
        validators = []

class DigitisationApplicationSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = DigitisationApplication
        fields = '__all__'

class VisitorGroupQRCodeSerializer(serializers.HyperlinkedModelSerializer, AutoUserModelSerializer):
    class Meta:
        model = VisitorGroupQRCode
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class SocialAppSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialApp
        fields = '__all__'

class SidebarMenuItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SidebarMenuItem
        fields = '__all__'

class ProductStatementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductStatement
        fields = '__all__'

class ProductAnnotationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductAnnotation
        fields = '__all__'

class QuestionnaireEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionnaireEntry
        fields = '__all__'

class QuestionnaireAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionnaireAnswer
        fields = '__all__'

class QuestionnaireQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionnaireQuestion
        fields = '__all__'
