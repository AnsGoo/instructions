from django.db.models import F
from rest_framework import filters, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from content.models import Document
from content.serializers import DocumentSerializer, DocumentUploadSerializer
from content.utils import get_file_md5, store_file


class DocumentViewSet(mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    """分类视图集，提供CRUD操作"""

    queryset = Document.objects.all().order_by('order')
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'type']

    @action(detail=False, methods=['post'], url_name='file-upload', url_path='upload')
    def upload(self, request):
        self.serializer_class = DocumentUploadSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        collection = serializer.validated_data['collection']
        file_data = request.FILES['file']
        bin_data = file_data.read()
        md5 = get_file_md5(bin_data)
        file_path, filecode = store_file(file.name, md5, bin_data)
        document = Document.objects.create(
            size=file.size,
            code=filecode,
            name=file.name,
            type=file.content_type,
            file=file_path,
            hexcode=md5,
            collection_id=collection,
            order=Document.objects.filter(collection_id=collection).count() + 1,
        )
        return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)
