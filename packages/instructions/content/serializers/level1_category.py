from rest_framework import serializers

from content.models import Level1Category


class Level1CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Level1Category
        fields = ['id', 'code', 'name', 'description']
