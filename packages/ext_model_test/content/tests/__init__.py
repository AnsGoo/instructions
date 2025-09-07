# 导入测试类
from .model_base import ExtModelTestProject
from .test_admin import AdminIntegrationTest, AttrDefinitionAdminTest, ModelDefinitionAdminTest
from .test_soft_delete import SoftDeleteTestSuite

__all__ = [
    'ExtModelTestProject',
    'AdminIntegrationTest',
    'AttrDefinitionAdminTest',
    'ModelDefinitionAdminTest',
    'SoftDeleteTestSuite',
]
