from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Level1CategoryViewSet, CategoryViewSet, ContentViewSet

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'level1-categories', Level1CategoryViewSet, basename='level1category')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'contents', ContentViewSet, basename='content')

# 将路由器的URL包含进来
urlpatterns = [
    path('', include(router.urls)),
]

# API端点汇总：
# - 一级分类：/api/level1-categories/
# - 分类：/api/categories/
# - 内容：/api/contents/
# 每个端点都支持GET, POST, PUT, PATCH, DELETE操作
# 还包括自定义操作，如：
# - 一级分类计数：/api/level1-categories/count/
# - 按一级分类获取分类：/api/categories/by_level1/?level1_id=id
# - 按分类获取内容：/api/contents/by_category/?category_id=id
# - 按状态获取内容：/api/contents/by_state/?state=状态值