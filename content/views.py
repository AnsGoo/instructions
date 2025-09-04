from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Level1Category, Category, Content
from .serializers import Level1CategorySerializer, CategorySerializer, ContentSerializer


class Level1CategoryViewSet(viewsets.ModelViewSet):
    """一级分类视图集，提供CRUD操作"""
    queryset = Level1Category.objects.all()
    serializer_class = Level1CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'description']
    
    def perform_create(self, serializer):
        """创建一级分类"""
        serializer.save()
    
    def perform_update(self, serializer):
        """更新一级分类"""
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        """获取一级分类总数"""
        count = self.get_queryset().count()
        return Response({'count': count})


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
    
    def perform_create(self, serializer):
        """创建分类，注意需要处理level1_id和definition_id"""
        serializer.save()
    
    def perform_update(self, serializer):
        """更新分类"""
        serializer.save()


class ContentViewSet(viewsets.ModelViewSet):
    """内容视图集，提供CRUD操作"""
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'title', 'abstract', 'summary', 'keyword', 'document_type', 'state', 'category__name']
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """根据分类获取内容列表"""
        category_id = request.query_params.get('category_id', None)
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                contents = self.get_queryset().filter(category=category)
                serializer = self.get_serializer(contents, many=True)
                return Response(serializer.data)
            except Category.DoesNotExist:
                return Response({'error': '分类不存在'}, status=404)
        return Response({'error': '缺少category_id参数'}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_state(self, request):
        """根据状态获取内容列表"""
        state = request.query_params.get('state', None)
        if state:
            contents = self.get_queryset().filter(state=state)
            serializer = self.get_serializer(contents, many=True)
            return Response(serializer.data)
        return Response({'error': '缺少state参数'}, status=400)
    
    def perform_create(self, serializer):
        """创建内容"""
        serializer.save()
    
    def perform_update(self, serializer):
        """更新内容"""
        serializer.save()
