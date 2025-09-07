from rest_framework import serializers

from content.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        exclude = ['order', 'is_delete', 'delete_at']
