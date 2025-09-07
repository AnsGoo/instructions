from django.urls import include, path
from rest_framework.routers import DefaultRouter, DynamicRoute, Route, SimpleRouter

from .views import CategoryViewSet, ContentViewSet, DocumentViewSet


# 为ContentViewSet创建自定义路由器
class CustomRouter(SimpleRouter):
    routes = [
        # 列表路由
        Route(
            url=r'^{prefix}/contents/$',
            mapping={'get': 'list', 'post': 'create'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'},
        ),
        # 详情路由
        Route(
            url=r'^{prefix}/contents/(?P<pk>[^/.]+)/$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy',
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'},
        ),
        # 动态路由
        DynamicRoute(
            url=r'^{prefix}/contents/(?P<url_path>[^/]+)/$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={},
        ),
    ]


# 创建默认路由器并注册视图集
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'documents', DocumentViewSet, basename='document')

# 创建自定义路由器并注册ContentViewSet
content_router = CustomRouter()
content_router.register(r'(?P<category_id>[^/.]+)', ContentViewSet, basename='content')

# 将路由器的URL包含进来
urlpatterns = [
    path('', include(router.urls)),
    path('', include(content_router.urls)),
]

# API端点汇总：
# - 分类：/api/categories/
# - 内容：/api/{category_id}/contents/
# 每个端点都支持GET, POST, PUT, PATCH, DELETE操作
# 还包括自定义操作，如：
# - 按一级分类获取分类：/api/categories/by_level1/?level1_id=id
# - 按状态获取内容：/api/{category_id}/contents/by_state/?state=状态值
