from rest_framework import serializers


class VertexSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    z = serializers.IntegerField()
