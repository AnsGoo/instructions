from django.contrib.auth.models import User
from django.db import connection
from django.db.models import CharField, Count, Value
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.test import TestCase

# 导入ext_model的模型
from ext_model.models import AttrDefinitionModel, ModelDefinitionModel


class SoftDeleteTestSuite(TestCase):
    """
    软删除功能测试套件
    专注于测试BaseModel的软删除功能在各种查询和管理方法中的行为
    """

    def setUp(self):
        """测试前的准备工作，创建测试数据"""
        # 创建一个测试用户
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_soft_delete_basic_functionality(self):
        """测试软删除的基本功能"""
        # 创建测试实例
        active_instance = ModelDefinitionModel.objects.create(
            name='活跃实例',
            code='active_instance',
            description='这个实例不会被删除',
            create_user=self.user,
            update_user=self.user,
        )

        deleted_instance = ModelDefinitionModel.objects.create(
            name='已删除实例',
            code='deleted_instance',
            description='这个实例将会被软删除',
            create_user=self.user,
            update_user=self.user,
        )

        # 执行软删除
        deleted_instance_id = deleted_instance.id
        deleted_instance.delete()

        # 验证软删除状态
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT is_delete, delete_at FROM attr_model WHERE id = %s', [deleted_instance_id]
            )
            result = cursor.fetchone()
            self.assertTrue(result[0])  # is_delete应该为True
            self.assertIsNotNone(result[1])  # delete_at应该有值

        # 验证查询不包含已删除的记录
        all_instances = ModelDefinitionModel.objects.all()
        self.assertEqual(len(all_instances), 1)
        self.assertTrue(all(instance.id == active_instance.id for instance in all_instances))

    def test_soft_delete_query_methods(self):
        """测试各种查询方法在软删除后的行为"""
        # 创建测试实例
        active_instance = ModelDefinitionModel.objects.create(
            name='活跃实例',
            code='active_instance',
            description='这个实例不会被删除',
            create_user=self.user,
            update_user=self.user,
        )

        deleted_instance = ModelDefinitionModel.objects.create(
            name='已删除实例',
            code='deleted_instance',
            description='这个实例将会被软删除',
            create_user=self.user,
            update_user=self.user,
        )

        # 执行软删除
        deleted_instance_id = deleted_instance.id
        deleted_instance.delete()

        # 1. all()方法
        self.assertEqual(ModelDefinitionModel.objects.all().count(), 1)

        # 2. filter()方法
        self.assertEqual(ModelDefinitionModel.objects.filter(id=active_instance.id).count(), 1)
        self.assertEqual(ModelDefinitionModel.objects.filter(id=deleted_instance_id).count(), 0)

        # 3. exclude()方法
        self.assertEqual(ModelDefinitionModel.objects.exclude(id=active_instance.id).count(), 0)

        # 4. get()方法
        try:
            ModelDefinitionModel.objects.get(id=active_instance.id)
        except ModelDefinitionModel.DoesNotExist:
            self.fail('get()方法未能找到未删除的实例')

        with self.assertRaises(ModelDefinitionModel.DoesNotExist):
            ModelDefinitionModel.objects.get(id=deleted_instance_id)

        # 5. distinct()方法
        self.assertEqual(ModelDefinitionModel.objects.distinct().count(), 1)

        # 6. order_by()方法
        ordered_instances = ModelDefinitionModel.objects.order_by('name')
        self.assertEqual(ordered_instances.count(), 1)

        # 7. reverse()方法
        reversed_instances = ModelDefinitionModel.objects.reverse()
        self.assertEqual(reversed_instances.count(), 1)

        # 8. values()方法
        values_instances = ModelDefinitionModel.objects.values()
        self.assertEqual(len(values_instances), 1)
        self.assertTrue(active_instance.id in [instance['id'] for instance in values_instances])

        # 9. values_list()方法
        values_list_instances = ModelDefinitionModel.objects.values_list('id')
        self.assertEqual(len(values_list_instances), 1)
        self.assertTrue(active_instance.id in [instance[0] for instance in values_list_instances])

        # 10. count()方法
        self.assertEqual(ModelDefinitionModel.objects.count(), 1)

        # 11. exists()方法
        self.assertTrue(ModelDefinitionModel.objects.filter(id=active_instance.id).exists())
        self.assertFalse(ModelDefinitionModel.objects.filter(id=deleted_instance_id).exists())

        # 12. first()和last()方法
        self.assertEqual(ModelDefinitionModel.objects.first().id, active_instance.id)
        self.assertEqual(ModelDefinitionModel.objects.last().id, active_instance.id)

    def test_soft_delete_manager_methods(self):
        """测试管理器方法在软删除后的行为"""
        # 创建测试实例
        active_instance = ModelDefinitionModel.objects.create(
            name='活跃实例',
            code='active_instance',
            description='这个实例不会被删除',
            create_user=self.user,
            update_user=self.user,
        )

        deleted_instance = ModelDefinitionModel.objects.create(
            name='已删除实例',
            code='deleted_instance',
            description='这个实例将会被软删除',
            create_user=self.user,
            update_user=self.user,
        )

        # 执行软删除
        deleted_instance_id = deleted_instance.id
        deleted_instance.delete()

        # 1. in_bulk()方法
        bulk_instances = ModelDefinitionModel.objects.in_bulk(
            [active_instance.id, deleted_instance_id]
        )
        self.assertEqual(len(bulk_instances), 1)
        self.assertIn(active_instance.id, bulk_instances)
        self.assertNotIn(deleted_instance_id, bulk_instances)

        # 2. iterator()方法
        iterator_count = sum(1 for _ in ModelDefinitionModel.objects.iterator())
        self.assertEqual(iterator_count, 1)

        # 3. aggregate()方法
        aggregate_result = ModelDefinitionModel.objects.aggregate(total=Count('id'))
        self.assertEqual(aggregate_result['total'], 1)

        # 4. update()方法
        ModelDefinitionModel.objects.update(name='更新后的名称')
        updated_instance = ModelDefinitionModel.objects.get(id=active_instance.id)
        self.assertEqual(updated_instance.name, '更新后的名称')

        # 验证已删除实例的名称没有被更新
        with connection.cursor() as cursor:
            cursor.execute('SELECT name FROM attr_model WHERE id = %s', [deleted_instance_id])
            result = cursor.fetchone()
            self.assertEqual(result[0], '已删除实例')  # 名称应该保持不变

    def test_soft_delete_queryset_methods(self):
        """测试QuerySet方法在软删除后的行为"""
        # 创建测试实例
        active_instance = ModelDefinitionModel.objects.create(
            name='活跃实例',
            code='active_instance',
            description='这个实例不会被删除',
            create_user=self.user,
            update_user=self.user,
        )

        deleted_instance = ModelDefinitionModel.objects.create(
            name='已删除实例',
            code='deleted_instance',
            description='这个实例将会被软删除',
            create_user=self.user,
            update_user=self.user,
        )

        # 执行软删除
        deleted_instance.delete()

        # 1. select_related()方法
        select_related_instances = ModelDefinitionModel.objects.select_related('create_user').all()
        self.assertEqual(len(select_related_instances), 1)

        # 2. prefetch_related()方法
        prefetch_related_instances = ModelDefinitionModel.objects.prefetch_related(
            'create_user'
        ).all()
        self.assertEqual(len(prefetch_related_instances), 1)

        # 3. defer()和only()方法
        defer_instances = ModelDefinitionModel.objects.defer('description').all()
        only_instances = ModelDefinitionModel.objects.only('name').all()
        self.assertEqual(len(defer_instances), 1)
        self.assertEqual(len(only_instances), 1)

        # 4. using()方法
        using_instances = ModelDefinitionModel.objects.using('default').all()
        self.assertEqual(len(using_instances), 1)

        # 5. none()方法
        none_instances = ModelDefinitionModel.objects.none()
        self.assertEqual(len(none_instances), 0)

        # 6. annotate()方法
        annotated_instances = ModelDefinitionModel.objects.annotate(
            test_field=Value('test', output_field=CharField())
        ).all()
        self.assertEqual(len(annotated_instances), 1)
        self.assertEqual(annotated_instances[0].test_field, 'test')

        # 7. union()方法
        query1 = ModelDefinitionModel.objects.filter(code='active_instance')
        query2 = ModelDefinitionModel.objects.filter(name='活跃实例')
        union_query = query1.union(query2)
        self.assertEqual(len(union_query), 1)

        # 8. explain()方法
        explain_result = ModelDefinitionModel.objects.filter(id=active_instance.id).explain()
        self.assertIsNotNone(explain_result)

    def test_soft_delete_with_related_models(self):
        """测试软删除在相关模型中的行为"""
        # 创建模型定义
        model_definition = ModelDefinitionModel.objects.create(
            name='测试模型',
            code='test_model',
            description='用于测试的模型定义',
            create_user=self.user,
            update_user=self.user,
        )

        # 创建相关的属性定义
        attr1 = AttrDefinitionModel.objects.create(
            attr_name='attr1',
            attr_id='attr1',
            attr_label='属性1',
            model=model_definition,
            create_user=self.user,
            update_user=self.user,
        )

        attr2 = AttrDefinitionModel.objects.create(
            attr_name='attr2',
            attr_id='attr2',
            attr_label='属性2',
            model=model_definition,
            create_user=self.user,
            update_user=self.user,
        )

        # 软删除模型定义
        model_definition.delete()

        # 验证模型定义已被软删除
        self.assertFalse(ModelDefinitionModel.objects.filter(id=model_definition.id).exists())

        # 验证相关的属性定义仍然存在
        # 注意：这里属性定义的外键是SET_NULL，所以即使模型定义被删除，属性定义仍然存在
        self.assertTrue(AttrDefinitionModel.objects.filter(id=attr1.id).exists())
        self.assertTrue(AttrDefinitionModel.objects.filter(id=attr2.id).exists())

    def test_soft_delete_get_object_or_404(self):
        """测试get_object_or_404函数在软删除后的行为"""
        # 创建测试实例
        active_instance = ModelDefinitionModel.objects.create(
            name='活跃实例',
            code='active_instance',
            description='这个实例不会被删除',
            create_user=self.user,
            update_user=self.user,
        )

        deleted_instance = ModelDefinitionModel.objects.create(
            name='已删除实例',
            code='deleted_instance',
            description='这个实例将会被软删除',
            create_user=self.user,
            update_user=self.user,
        )

        # 执行软删除
        deleted_instance.delete()

        # 测试获取未删除的实例
        retrieved_instance = get_object_or_404(ModelDefinitionModel, id=active_instance.id)
        self.assertEqual(retrieved_instance.id, active_instance.id)

        # 测试获取已删除的实例应该抛出Http404
        with self.assertRaises(Http404):
            get_object_or_404(ModelDefinitionModel, id=deleted_instance.id)
