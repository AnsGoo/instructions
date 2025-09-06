from ast import Raise
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Level1Category, Category, Content
from .serializers import Level1CategorySerializer, CategorySerializer, ContentSerializer
from core.models import AttrDefinitionModel


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
    """内容视图集，提供CRUD操作，强制要求category信息"""
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'title', 'abstract', 'summary', 'keyword', 'document_type', 'state']
    
    def initialize_request(self, request, *args, **kwargs):
        """初始化请求，添加category_id到kwargs"""
        category_id = self.kwargs.get('category_id')
        try:
            # 验证分类是否存在
            category = Category.objects.filter(id=category_id).first()
            ext_fields = AttrDefinitionModel.objects.filter(model=category.definition_id)
            request.ext_fields = ext_fields
            request.definition_id = category.definition_id
        except Category.DoesNotExist:
           raise Exception('指定的分类不存在')
        
        return super().initialize_request(request, *args, **kwargs)

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
        category_id = self.kwargs.get('category_id')
        if not category_id:
            return Response({'error': '缺少category_id参数'}, status=400)
            
        try:
            # 验证分类是否存在
            category = Category.objects.get(id=category_id)
            # 在请求数据中添加分类信息
            request.data['category_id'] = category_id
        except Category.DoesNotExist:
            return Response({'error': '指定的分类不存在'}, status=404)
            
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def by_state(self, request, category_id=None):
        """根据状态和分类获取内容列表"""
        state = request.query_params.get('state', None)
        if not state:
            return Response({'error': '缺少state参数'}, status=400)
            
        # 确保内容属于指定分类
        contents = self.get_queryset().filter(state=state)
        serializer = self.get_serializer(contents, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """创建内容，自动设置创建用户和关联分类"""
        category_id = self.kwargs.get('category_id')
        # 确保关联到正确的分类
        if category_id:
            serializer.save(create_user=self.request.user, category_id=category_id)
        else:
            serializer.save(create_user=self.request.user)
    
    def perform_update(self, serializer):
        """更新内容，自动设置更新用户，确保分类不变"""
        category_id = self.kwargs.get('category_id')
        # 确保更新时不会更改分类
        if category_id:
            serializer.save(update_user=self.request.user, category_id=category_id)
        else:
            serializer.save(update_user=self.request.user)
