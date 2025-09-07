# 导入测试类
from .model_base import ExtModelTestProject
from .test_admin import AdminIntegrationTest, AttrDefinitionAdminTest, ModelDefinitionAdminTest

__all__ = [
    'ExtModelTestProject',
    'AdminIntegrationTest',
    'AttrDefinitionAdminTest',
    'ModelDefinitionAdminTest',
]
