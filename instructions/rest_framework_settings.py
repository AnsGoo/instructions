from rest_framework import pagination
from rest_framework.permissions import BasePermission


class StandardResultsSetPagination(pagination.PageNumberPagination):
    """自定义分页类，设置默认每页显示条数和最大每页显示条数"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ReadOnly(BasePermission):
    """只读权限类，允许所有人读取数据"""

    def has_permission(self, request, view):
        return request.method in ("GET", "HEAD", "OPTIONS")


# 全局REST框架配置
def get_rest_framework_settings():
    return {
        # 默认分页类
        "DEFAULT_PAGINATION_CLASS": "instructions.rest_framework_settings.StandardResultsSetPagination",
        # 默认认证类
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.BasicAuthentication",
        ],
        # 默认权限类
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.AllowAny",  # 允许任何用户访问，可根据需要调整
        ],
        # 默认渲染器类
        "DEFAULT_RENDERER_CLASSES": [
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",  # 启用可浏览的API界面
        ],
        # 默认过滤器后端
        "DEFAULT_FILTER_BACKENDS": [
            "rest_framework.filters.SearchFilter",
            "rest_framework.filters.OrderingFilter",
        ],
        # 默认版本控制类
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
        "DEFAULT_VERSION": "v1",
        "ALLOWED_VERSIONS": ["v1"],
        "VERSION_PARAM": "version",
        # 测试请求头
        "TEST_REQUEST_DEFAULT_FORMAT": "json",
        # 浏览API界面设置
        "URL_FIELD_NAME": "url",
    }
