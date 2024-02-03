from rest_framework import serializers
from vis.models import ThreeDimensionalMesh


class VertexSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    z = serializers.IntegerField()
