from rest_framework import serializers

from content.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ['order', 'is_delete', 'delete_at']


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=200, allow_empty_file=False)
    collection = serializers.IntegerField(required=True, allow_null=False)
