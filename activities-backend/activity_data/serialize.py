from rest_framework import serializers
from activity_data.models import Product
from activity_data.models import Visitor

class Productserialize(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
class Visitorserialize(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"
        