from django.contrib.auth.models import User
from django.db import IntegrityError, connection
from django.http import Http404
from django.test import TestCase
from django.shortcuts import get_object_or_404

# 导入ext_model的模型
from ..models import AttrDefinitionModel, ExtModel, ModelDefinitionModel


class ExtModelTestProject(TestCase):
    """
    ext_model 基础库测试工程
    提供对ext_model中各种模型和功能的测试用例
    """

    def setUp(self):
        """测试前的准备工作，创建测试数据"""
        # 创建一个测试用户
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # 创建一个模型定义
        self.model_definition = ModelDefinitionModel.objects.create(
            name='测试模型',
            code='test_model',
            description='这是一个测试模型',
            create_user=self.user,
            update_user=self.user,
        )

        # 创建几个属性定义
        self.attr_definition1 = AttrDefinitionModel.objects.create(
            attr_name='test_attr1',
            attr_id='attr1',
            attr_label='测试属性1',
            attr_description='这是测试属性1的描述',
            model=self.model_definition,
            create_user=self.user,
            update_user=self.user,
        )

        self.attr_definition2 = AttrDefinitionModel.objects.create(
            attr_name='test_attr2',
            attr_id='attr2',
            attr_label='测试属性2',
            attr_description='这是测试属性2的描述',
            model=self.model_definition,
            create_user=self.user,
            update_user=self.user,
        )

    def test_basemodel_soft_delete(self):
        """测试BaseModel的软删除功能"""
        # 创建一个模型定义实例
        model_instance = ModelDefinitionModel.objects.create(
            name='测试软删除',
            code='soft_delete_test',
            description='用于测试软删除功能',
            create_user=self.user,
            update_user=self.user,
        )

        # 获取创建的实例
        self.assertTrue(ModelDefinitionModel.objects.filter(id=model_instance.id).exists())

        # 执行软删除
        model_instance.delete()
        # 检查是否触发了信号（即软删除后使用get方法应该抛出DoesNotExist异常）
        with self.assertRaises(ModelDefinitionModel.DoesNotExist):
            ModelDefinitionModel.objects.get(id=model_instance.id)

        # 使用get_object_or_404获取实例
        with self.assertRaises(Http404):
            get_object_or_404(ModelDefinitionModel, id=model_instance.id)
        # 验证实例已被标记为删除但仍存在于数据库中
        self.assertFalse(ModelDefinitionModel.objects.filter(id=model_instance.id).exists())

        # 使用Django原始查询验证实例仍然存在且is_delete为True

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT is_delete, delete_at FROM attr_model WHERE id = %s', [model_instance.id]
            )
            result = cursor.fetchone()
            self.assertTrue(result[0])  # is_delete应该为True
            self.assertIsNotNone(result[1])  # delete_at应该有值

    def test_model_definition_crud(self):
        """测试ModelDefinitionModel的CRUD操作"""
        # CREATE - 在setUp中已经创建了model_definition

        # READ
        retrieved_model = ModelDefinitionModel.objects.get(id=self.model_definition.id)
        self.assertEqual(retrieved_model.name, '测试模型')
        self.assertEqual(retrieved_model.code, 'test_model')

        # UPDATE
        retrieved_model.name = '更新后的模型名称'
        retrieved_model.save()
        updated_model = ModelDefinitionModel.objects.get(id=self.model_definition.id)
        self.assertEqual(updated_model.name, '更新后的模型名称')

        # DELETE
        retrieved_model.delete()
        self.assertFalse(ModelDefinitionModel.objects.filter(id=self.model_definition.id).exists())

    def test_attr_definition_crud(self):
        """测试AttrDefinitionModel的CRUD操作"""
        # CREATE - 在setUp中已经创建了attr_definition1和attr_definition2

        # READ
        retrieved_attr = AttrDefinitionModel.objects.get(id=self.attr_definition1.id)
        self.assertEqual(retrieved_attr.attr_name, 'test_attr1')
        self.assertEqual(retrieved_attr.attr_label, '测试属性1')
        self.assertEqual(retrieved_attr.model, self.model_definition)

        # UPDATE
        retrieved_attr.attr_label = '更新后的属性1'
        retrieved_attr.save()
        updated_attr = AttrDefinitionModel.objects.get(id=self.attr_definition1.id)
        self.assertEqual(updated_attr.attr_label, '更新后的属性1')

        # DELETE
        retrieved_attr.delete()
        self.assertFalse(AttrDefinitionModel.objects.filter(id=self.attr_definition1.id).exists())

    def test_attr_definition_unique_constraint(self):
        """测试AttrDefinitionModel的(model, attr_id)唯一约束"""
        # 尝试创建具有相同model和attr_id的属性定义，应该引发IntegrityError

        with self.assertRaises(IntegrityError):
            AttrDefinitionModel.objects.create(
                attr_name='duplicate_attr',
                attr_id=self.attr_definition2.attr_id,  # 使用相同的attr_id
                attr_label='重复属性',
                model=self.model_definition,  # 使用相同的model
                create_user=self.user,
                update_user=self.user,
            )

    def test_extmodel_functionality(self):
        """测试ExtModel的功能"""

        # 创建一个ExtModel的具体子类用于测试
        class ConcreteExtModel(ExtModel):
            """测试用的具体ExtModel子类"""

            model_id = None

            def get_instance_model_id(self):
                """实现必要的抽象方法"""
                return self.model_id

        # 创建测试实例
        test_instance = ConcreteExtModel()
        test_instance.model_id = self.model_definition.id

        # 测试获取扩展字段定义
        ext_fields = test_instance.get_extended_field_definitions()
        self.assertEqual(len(ext_fields), 2)  # 应该有两个属性定义
        self.assertIn('test_attr1', ext_fields)
        self.assertIn('test_attr2', ext_fields)

    def test_model_manager(self):
        """测试自定义的BaseManger"""
        # 测试普通查询不包含已删除的记录
        model_instance = ModelDefinitionModel.objects.create(
            name='测试管理器',
            code='manager_test',
            description='用于测试管理器功能',
            create_user=self.user,
            update_user=self.user,
        )

        # 获取所有未删除的记录数量
        initial_count = ModelDefinitionModel.objects.count()

        # 软删除一条记录
        model_instance.delete()

        # 验证查询结果不包含已删除的记录
        after_delete_count = ModelDefinitionModel.objects.count()
        self.assertEqual(after_delete_count, initial_count - 1)

    def test_base_model_inheritance(self):
        """测试BaseModel的继承功能"""
        # 由于动态创建的模型没有数据库表，我们使用现有的ModelDefinitionModel来测试继承
        # ModelDefinitionModel继承自BaseModel，所以可以用来测试继承的字段和方法

        # 创建一个ModelDefinitionModel实例
        model_instance = ModelDefinitionModel.objects.create(
            name='测试继承',
            code='inheritance_test',
            description='用于测试继承功能',
            create_user=self.user,
            update_user=self.user,
        )

        # 验证继承的字段
        self.assertIsNotNone(model_instance.create_time)
        self.assertIsNotNone(model_instance.update_time)
        self.assertFalse(model_instance.is_delete)
        self.assertEqual(model_instance.create_user, self.user)
        self.assertEqual(model_instance.update_user, self.user)

        # 验证继承的方法
        model_instance.delete()
        self.assertTrue(model_instance.is_delete)
        self.assertIsNotNone(model_instance.delete_at)

    def test_model_and_attr_relationship(self):
        """测试模型定义和属性定义之间的关系"""
        # 获取与模型关联的所有属性
        model_attrs = self.model_definition.attrdefinitionmodel_model.all()

        # 验证关系
        self.assertEqual(model_attrs.count(), 2)
        attr_names = [attr.attr_name for attr in model_attrs]
        self.assertIn('test_attr1', attr_names)
        self.assertIn('test_attr2', attr_names)
