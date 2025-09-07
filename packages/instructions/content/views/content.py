from ext_model.models import AttrDefinitionModel
from rest_framework import filters, status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from content.models import Category, Content
from content.serializers import ContentSerializer


class ModelDefinitionNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Model definition not found.'
    default_code = 'model_not_found'


class ContentViewSet(viewsets.ModelViewSet):
    """内容视图集，提供CRUD操作，强制要求category信息"""

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'title', 'abstract', 'summary', 'keyword', 'document_type', 'state']

    def initialize_request(self, request, *args, **kwargs):
        """初始化请求，检查category_id是否存在"""
        request.ext_fields = []
        request.definition_id = ''
        return super().initialize_request(request, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        try:
            category_id = self.kwargs.get('category_id')
            category = Category.objects.filter(id=category_id).first()
            ext_fields = AttrDefinitionModel.objects.filter(model=category.definition_id)
            self.kwargs.setdefault('definition_id', category.definition_id)
            self.kwargs.setdefault('ext_fields', ext_fields)
        except Category.DoesNotExist:
            raise ModelDefinitionNotFound('指定的分类不存在') from None
        return super().initial(request, *args, **kwargs)

    def get_queryset(self):
        """获取查询集，根据URL中的category_id过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def list(self, request, *args, **kwargs):
        """列出内容，强制关联到指定分类"""
        # 验证category_id是否存在
        category_id = self.kwargs.get('category_id')
        if not category_id:
            return Response({'error': '缺少category_id参数'}, status=400)

        try:
            # 验证分类是否存在
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error': '指定的分类不存在'}, status=404)

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """创建内容，自动关联到URL中的分类"""

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """创建内容，自动设置创建用户和关联分类"""
        serializer.save(create_user=self.request.user, **self.kwargs)

    def perform_update(self, serializer):
        """更新内容，自动设置更新用户"""
        serializer.save(update_user=self.request.user, **self.kwargs)
