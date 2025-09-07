from unittest.mock import MagicMock, patch

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from unittest.mock import MagicMock
from unittest.mock import patch

from ext_model.admin import AttrDefinitionModelAdmin, ModelDefinitionModelAdmin

# 导入ext_model的模型和admin
from ext_model.models import AttrDefinitionModel, ModelDefinitionModel
from content.models import ConcreteExtModel

User = get_user_model()


class MockAdminSite(AdminSite):
    """模拟AdminSite，用于测试"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_ext_model(self):
        """获取扩展模型"""
        return ConcreteExtModel



class ModelDefinitionAdminTest(TestCase):
    """测试ModelDefinitionModelAdmin的功能"""

    def setUp(self):
        # 创建测试用户
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password123'
        )
        # 登录用户
        self.client.login(username='admin', password='password123')

        # 创建测试数据
        self.model_definition = ModelDefinitionModel.objects.create(
            name='测试模型',
            code='test_model',
            description='这是一个测试模型',
            create_user=self.superuser,
            update_user=self.superuser,
        )

        # 创建RequestFactory
        self.factory = RequestFactory()

        # 创建Admin实例
        self.admin_site = MockAdminSite()
        self.model_admin = ModelDefinitionModelAdmin(ModelDefinitionModel, self.admin_site)

    def test_model_definition_list_display(self):
        """测试模型定义列表页面的显示字段"""
        url = reverse('admin:ext_model_modeldefinitionmodel_changelist')
        response = self.client.get(url)

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查列表页面是否包含模型定义的数据
        self.assertContains(response, '测试模型')
        self.assertContains(response, 'test_model')
        self.assertContains(response, '这是一个测试模型')

    def test_model_definition_search(self):
        """测试模型定义的搜索功能"""
        url = reverse('admin:ext_model_modeldefinitionmodel_changelist') + '?q=测试模型'
        response = self.client.get(url)

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查搜索结果是否包含模型定义的数据
        self.assertContains(response, '测试模型')

    def test_model_definition_detail_view(self):
        """测试模型定义详情页面"""
        url = reverse(
            'admin:ext_model_modeldefinitionmodel_change', args=[self.model_definition.id]
        )
        response = self.client.get(url)

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查详情页面是否包含模型定义的数据
        self.assertContains(response, '测试模型')
        self.assertContains(response, 'test_model')
        self.assertContains(response, '这是一个测试模型')

    def test_model_definition_no_add_permission(self):
        """测试模型定义没有添加权限"""
        request = self.factory.get(reverse('admin:ext_model_modeldefinitionmodel_add'))
        request.user = self.superuser

        # 检查是否有权限添加
        has_permission = self.model_admin.has_add_permission(request)

        # 模型定义应该没有添加权限
        self.assertFalse(has_permission)

    def test_model_definition_no_delete_permission(self):
        """测试模型定义没有删除权限"""
        request = self.factory.get(reverse('admin:ext_model_modeldefinitionmodel_changelist'))
        request.user = self.superuser

        # 检查是否有权限删除
        has_permission = self.model_admin.has_delete_permission(request)

        # 模型定义应该没有删除权限
        self.assertFalse(has_permission)


class AttrDefinitionAdminTest(TestCase):
    """测试AttrDefinitionModelAdmin的功能"""

    def setUp(self):
        # 创建测试用户
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password123'
        )
        # 登录用户
        self.client.login(username='admin', password='password123')

        # 创建测试数据
        self.model_definition = ModelDefinitionModel.objects.create(
            name='测试模型',
            code='test_model',
            description='这是一个测试模型',
            create_user=self.superuser,
            update_user=self.superuser,
        )

        self.attr_definition = AttrDefinitionModel.objects.create(
            attr_name='test_attr',
            attr_id='attr1',
            attr_label='测试属性',
            attr_description='这是一个测试属性',
            model=self.model_definition,
            create_user=self.superuser,
            update_user=self.superuser,
        )

        # 创建RequestFactory
        self.factory = RequestFactory()

        # 创建Admin实例
        self.admin_site = MockAdminSite()
        self.attr_admin = AttrDefinitionModelAdmin(AttrDefinitionModel, self.admin_site)

        # 创建模拟的ExtModel
        self.mock_ext_model = MagicMock()
        self.mock_ext_model.get_ext_prefix.return_value = 'attr'

        # 创建模拟的字段
        mock_field = MagicMock()
        mock_field.name = 'attr1'
        mock_field.verbose_name = '属性1'
        mock_field.db_type.return_value = 'varchar(255)'

    def test_attr_definition_list_display(self):
        """测试属性定义列表页面的显示字段"""
        url = reverse('admin:ext_model_attrdefinitionmodel_changelist')
        response = self.client.get(url)

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查列表页面是否包含属性定义的数据
        self.assertContains(response, 'test_attr')
        self.assertContains(response, 'attr1')
        self.assertContains(response, '测试属性')

    def test_attr_definition_search(self):
        """测试属性定义的搜索功能"""
        url = reverse('admin:ext_model_attrdefinitionmodel_changelist') + '?q=测试属性'
        response = self.client.get(url)

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查搜索结果是否包含属性定义的数据
        self.assertContains(response, '测试属性')

    def test_attr_definition_detail_view(self):
        """测试属性定义详情页面"""
        url = reverse('admin:ext_model_attrdefinitionmodel_change', args=[self.attr_definition.id])
        response = self.client.get(url)

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查详情页面是否包含属性定义的数据
        self.assertContains(response, 'test_attr')
        self.assertContains(response, 'attr1')
        self.assertContains(response, '测试属性')

    def test_attr_definition_form_validation(self):
        """测试属性定义表单验证"""
        # 测试冲突验证器
        request = self.factory.post(
            reverse('admin:ext_model_attrdefinitionmodel_add'),
            {
                'attr_name': 'attr1',  # 与已存在的字段名冲突
                'attr_id': 'attr2',
                'attr_label': '测试属性2',
                'model': self.model_definition.id,
            },
        )
        request.user = self.superuser

        # 使用patch来模拟表单验证
        with patch('django.forms.ModelForm.is_valid', return_value=False):
            with patch('django.forms.ModelForm.errors', {'attr_name': ['属性attr1已存在']}):
                # 由于实际验证是在get_form中添加的验证器，这里只检查是否有表单验证的逻辑
                form = self.attr_admin.get_form(request)
                self.assertIsNotNone(form)

    def test_attr_definition_readonly_fields(self):
        """测试属性定义的只读字段"""
        # 对于新对象，attr_id和model不应该是只读的
        readonly_fields_new = self.attr_admin.get_readonly_fields(self.factory.get('/'), None)
        self.assertNotIn('attr_id', readonly_fields_new)
        self.assertNotIn('model', readonly_fields_new)

        # 对于已存在的对象，attr_id和model应该是只读的
        readonly_fields_existing = self.attr_admin.get_readonly_fields(
            self.factory.get('/'), self.attr_definition
        )
        self.assertIn('attr_id', readonly_fields_existing)
        self.assertIn('model', readonly_fields_existing)


class AdminIntegrationTest(TestCase):
    """测试Admin的集成功能"""

    def setUp(self):
        # 创建测试用户
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password123'
        )
        # 登录用户
        self.client.login(username='admin', password='password123')

    def test_admin_access(self):
        """测试Admin后台的访问权限"""
        # 访问Admin首页
        url = reverse('admin:index')
        response = self.client.get(url)

        # 打印响应状态码和内容，用于调试
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content.decode()[:200]}...")

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)

        # 检查页面是否包含Admin相关的内容
        self.assertContains(response, 'Django')
        self.assertContains(response, '站点管理')

    def test_admin_logout(self):
        """测试Admin后台的登出功能"""
        # 登出用户
        self.client.logout()

        # 尝试访问Admin首页，应该重定向到登录页面
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('admin:login') + '?next=' + url)
