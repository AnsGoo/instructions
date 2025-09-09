from hmac import new

from django.contrib.auth.models import User
from django.db import IntegrityError, connection
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.test import TestCase

# 导入content应用中实现的模型
from content.models import ConcreteExtModel, MyAttrDefinitionModel, MyModelDefinitionModel


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
        self.model_definition = MyModelDefinitionModel.objects.create(
            name='测试模型', code='test_model', description='这是一个测试模型'
        )

        # 创建几个属性定义
        self.attr_definition1 = MyAttrDefinitionModel.objects.create(
            attr_name='test_attr1',
            attr_id='attr1',
            attr_label='测试属性1',
            attr_description='这是测试属性1的描述',
            model=self.model_definition,
        )

        self.attr_definition2 = MyAttrDefinitionModel.objects.create(
            attr_name='test_attr2',
            attr_id='attr2',
            attr_label='测试属性2',
            attr_description='这是测试属性2的描述',
            model=self.model_definition,
        )

    def test_model_definition_crud(self):
        """测试ModelDefinitionModel的CRUD操作"""
        # CREATE - 在setUp中已经创建了model_definition

        # READ
        retrieved_model = MyModelDefinitionModel.objects.get(id=self.model_definition.id)
        self.assertEqual(retrieved_model.name, '测试模型')
        self.assertEqual(retrieved_model.code, 'test_model')

        # UPDATE
        retrieved_model.name = '更新后的模型名称'
        retrieved_model.save()
        updated_model = MyModelDefinitionModel.objects.get(id=self.model_definition.id)
        self.assertEqual(updated_model.name, '更新后的模型名称')

        # DELETE
        retrieved_model.delete()
        self.assertFalse(
            MyModelDefinitionModel.objects.filter(id=self.model_definition.id).exists()
        )

    def test_attr_definition_crud(self):
        """测试AttrDefinitionModel的CRUD操作"""
        # CREATE - 在setUp中已经创建了attr_definition1和attr_definition2

        # READ
        retrieved_attr = MyAttrDefinitionModel.objects.get(id=self.attr_definition1.id)
        self.assertEqual(retrieved_attr.attr_name, 'test_attr1')
        self.assertEqual(retrieved_attr.attr_label, '测试属性1')
        self.assertEqual(retrieved_attr.model, self.model_definition)

        # UPDATE
        retrieved_attr.attr_label = '更新后的属性1'
        retrieved_attr.save()
        updated_attr = MyAttrDefinitionModel.objects.get(id=self.attr_definition1.id)
        self.assertEqual(updated_attr.attr_label, '更新后的属性1')

        # DELETE
        retrieved_attr.delete()
        self.assertFalse(MyAttrDefinitionModel.objects.filter(id=self.attr_definition1.id).exists())

    def test_attr_definition_unique_constraint(self):
        """测试AttrDefinitionModel的(model, attr_id)唯一约束"""
        # 尝试创建具有相同model和attr_id的属性定义，应该引发IntegrityError

        with self.assertRaises(IntegrityError):
            MyAttrDefinitionModel.objects.create(
                attr_name='duplicate_attr',
                attr_id=self.attr_definition2.attr_id,  # 使用相同的attr_id
                attr_label='重复属性',
                model=self.model_definition,  # 使用相同的model
            )

    def test_extmodel_functionality(self):
        """测试ExtModel的功能"""
        # 创建测试实例
        test_instance = ConcreteExtModel()
        test_instance.model_id = self.model_definition.id

        # 测试获取扩展字段定义
        ext_fields = test_instance.get_ext_field_definitions()
        self.assertEqual(len(ext_fields), 2)  # 应该有两个属性定义
        self.assertIn('test_attr1', ext_fields)
        self.assertIn('test_attr2', ext_fields)
        test_instance.update_ext_fields({'test_attr1': 'test_value1'})
        self.assertEqual(test_instance.attr1, 'test_value1')

    def test_extmodel_functionality_with_definition(self):
        """测试ExtModel的功能"""
        # 创建测试实例
        test_instance = ConcreteExtModel(
            code='test_model', name='测试模型', description='测试模型描述'
        )
        test_instance.definition = self.model_definition
        test_instance.model_id = self.model_definition.id  # 显式设置model_id以确保能找到属性定义
        test_instance.save()
        self.assertIsNotNone(test_instance.pk)
        self.assertEqual(ConcreteExtModel.objects.filter(pk=test_instance.pk).exists(), True)

        # 不保存到数据库，因为动态创建的模型没有数据库表
        # 直接测试内存中的对象属性和方法
        self.assertEqual(test_instance.definition, self.model_definition)

        # 测试获取扩展字段定义
        ext_fields = test_instance.get_ext_field_definitions()
        self.assertEqual(len(ext_fields), 2)  # 应该有两个属性定义
        self.assertIn('test_attr1', ext_fields)
        self.assertIn('test_attr2', ext_fields)
        test_instance.update_ext_fields({'test_attr1': 'test_value1'})
        test_instance.save()
        new_instance = ConcreteExtModel.objects.get(pk=test_instance.pk)
        self.assertEqual(new_instance.attr1, 'test_value1')

        new_instance.update_ext_fields({'test_attr3': 'test_value3'})
        new_instance.save()

        self.assertEqual(ConcreteExtModel.objects.get(pk=test_instance.pk).attr3, None)

    def test_model_manager(self):
        """测试自定义的BaseManger"""
        # 测试普通查询不包含已删除的记录
        model_instance = MyModelDefinitionModel.objects.create(
            name='测试管理器', code='manager_test', description='用于测试管理器功能'
        )

        # 获取所有未删除的记录数量
        initial_count = MyModelDefinitionModel.objects.count()

        # 软删除一条记录
        model_instance.delete()

        # 验证查询结果不包含已删除的记录
        after_delete_count = MyModelDefinitionModel.objects.count()
        self.assertEqual(after_delete_count, initial_count - 1)

    def test_base_model_inheritance(self):
        """测试BaseModel的继承功能"""
        # ModelDefinitionModel不继承自BaseModel，此测试方法暂时注释
        pass

    def test_model_and_attr_relationship(self):
        """测试模型定义和属性定义之间的关系"""
        # 获取与模型关联的所有属性
        model_attrs = self.model_definition.myattrdefinitionmodel_set.all()

        # 验证关系
        self.assertEqual(model_attrs.count(), 2)
        attr_names = [attr.attr_name for attr in model_attrs]
        self.assertIn('test_attr1', attr_names)
        self.assertIn('test_attr2', attr_names)
