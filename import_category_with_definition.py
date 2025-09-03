#!/usr/bin/env python
import os
import json
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instructions.settings')

import django
django.setup()

from content.models import Category, Level1Category
from core.models import AttrDefinitionModel
from django.utils import timezone


def import_categories_with_definition(fixture_path):
    """导入分类数据并自动生成关联的定义对象"""
    # 读取fixture文件
    with open(fixture_path, 'r', encoding='utf-8') as f:
        fixtures = json.load(f)
    
    # 记录创建的对象数量
    created_definitions = 0
    updated_categories = 0
    
    # 遍历每个category fixture
    for fixture in fixtures:
        if fixture['model'] == 'content.category':
            fields = fixture['fields']
            pk = fixture['pk']
            
            # 获取或创建Category对象
            try:
                category = Category.objects.get(pk=pk)
                print(f"找到分类 {pk}: {fields['name']}")
            except Category.DoesNotExist:
                # 如果不存在，创建新的Category对象
                level1 = Level1Category.objects.get(pk=fields['level1'])
                category = Category(
                    pk=pk,
                    code=fields['code'],
                    name=fields['name'],
                    description=fields['description'],
                    level1=level1,
                    is_delete=fields['is_delete']
                )
                print(f"创建新分类 {pk}: {fields['name']}")
            
            # 检查是否已有关联的definition
            if not category.definition:
                # 创建对应的AttrDefinitionModel对象
                attr_definition = AttrDefinitionModel(
                    attr_type='text',  # 默认使用text类型
                    attr_name=f"分类_{fields['code']}_定义",
                    attr_id=f"category_{fields['code']}",
                    attr_description=f"分类'{fields['name']}'的属性定义"
                )
                attr_definition.save()
                created_definitions += 1
                
                # 关联definition到category
                category.definition = attr_definition
                category.save()
                updated_categories += 1
                print(f"  ✅ 为分类 {fields['name']} 创建并关联了定义对象")
            else:
                print(f"  分类 {fields['name']} 已有关联的定义对象")
    
    # 输出统计信息
    print(f"\n导入完成！")
    print(f"- 创建了 {created_definitions} 个定义对象")
    print(f"- 更新了 {updated_categories} 个分类对象")


if __name__ == '__main__':
    # 默认fixture路径
    default_fixture_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'content', 'fixtures', 'category_coto_fixture.json'
    )
    
    # 如果提供了命令行参数，使用指定的fixture路径
    fixture_path = sys.argv[1] if len(sys.argv) > 1 else default_fixture_path
    
    print(f"开始导入分类数据并自动生成定义对象...")
    print(f"使用fixture文件: {fixture_path}")
    
    if not os.path.exists(fixture_path):
        print(f"错误: 找不到fixture文件 {fixture_path}")
        sys.exit(1)
    
    import_categories_with_definition(fixture_path)
    print("\n操作完成！")