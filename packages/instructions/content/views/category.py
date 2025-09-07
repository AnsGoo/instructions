from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from content.models import Category, Level1Category
from content.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集，提供CRUD操作"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'description', 'level1__name', 'level1__code']

    @action(detail=False, methods=['get'])
    def by_level1(self, request):
        """根据一级分类获取分类列表"""
        level1_id = request.query_params.get('level1_id', None)
        if level1_id:
            try:
                level1 = Level1Category.objects.get(id=level1_id)
                categories = self.get_queryset().filter(level1=level1)
                serializer = self.get_serializer(categories, many=True)
                return Response(serializer.data)
            except Level1Category.DoesNotExist:
                return Response({'error': '一级分类不存在'}, status=404)
        return Response({'error': '缺少level1_id参数'}, status=400)
