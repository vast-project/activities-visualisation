from rest_framework import serializers

class SparqlQuerySerializer(serializers.Serializer):
    q = serializers.CharField()

    def create(self, validated_data):
        return SparqlQuery(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
