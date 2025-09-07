from rest_framework import filters, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from content.models import Document
from content.serializers import DocumentSerializer


class DocumentViewSet(mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    """分类视图集，提供CRUD操作"""

    queryset = Document.objects.all().order_by('order')
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'type']

    @action(detail=False, methods=['post'], url_name='file-upload', url_path='upload')
    def upload(self, request):
        """上传文件"""
        file = request.FILES['file']
        collection = request.data.get('collection')
        document = Document.objects.create(
            name=file.name,
            type=file.content_type,
            file=file,
            collection_id=collection,
            order=Document.objects.filter(collection_id=collection).count() + 1,
        )
        return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)
